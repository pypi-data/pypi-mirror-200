import datetime

from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Tuple

from ncei_cruise_schema.entity.access_path import AccessPath
from ncei_cruise_schema.entity.contact import Contact
from ncei_cruise_schema.entity.dataset import Dataset
from ncei_cruise_schema.entity.instrument import Instrument
from ncei_cruise_schema.entity.platform import Platform
from ncei_cruise_schema.entity.survey import Survey
from ncei_cruise_schema.orm.entity import Entity

from src.mb_cruise_migration.db.cruise_db import CruiseDb
from src.mb_cruise_migration.framework.cache import Cache
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.logging.migration_report import MigrationReport
from src.mb_cruise_migration.models.cruise.cruise_access_path import CruiseAccessPath
from src.mb_cruise_migration.models.cruise.cruise_instruments import CruiseInstrument
from src.mb_cruise_migration.models.cruise.cruise_people_and_sources import CruisePeopleAndSources
from src.mb_cruise_migration.models.cruise.cruise_platforms import CruisePlatform
from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseCargo, \
    CruiseSurveyCrate, CruiseDatasetCrate, CruiseProjectCrate, CruiseFileCrate
from src.mb_cruise_migration.models.intermediary.migrating_survey import MigratingSurvey
from src.mb_cruise_migration.services.cruise_service import ParameterService, SurveyService, \
    DatasetService, ContactService, InstrumentService, PlatformService, \
    ProjectService, FileService, AccessPathService, ShapeService, BatchService
from src.mb_cruise_migration.utility.common import strip_none


class CruiseProcessor(object):
    survey_cache = Cache()
    platform_cache = Cache()
    scientist_cache = Cache()
    source_cache = Cache()
    project_cache = Cache()
    instrument_cache = Cache()

    def __init__(self):
        db = CruiseDb(MigrationProperties.cruise_db_config.pooled)
        self.parameter_service = ParameterService(db)
        self.survey_service = SurveyService(db)
        self.dataset_service = DatasetService(db)
        self.contact_service = ContactService(db)
        self.instrument_service = InstrumentService(db)
        self.platform_service = PlatformService(db)
        self.project_service = ProjectService(db)
        self.file_service = FileService(db)
        self.access_path_service = AccessPathService(db)
        self.shape_service = ShapeService(db)
        self.batch_service = BatchService()
        self.survey_parameters = []
        self.dataset_parameters = []
        self.dataset_survey_mappings = []
        self.dataset_scientist_mappings = []
        self.dataset_source_mappings = []
        self.dataset_platform_mappings = []
        self.dataset_instrument_mappings = []
        self.dataset_project_mappings = []
        self.file_parameters = []
        self.file_access_path_mappings = []
        self.access_path_cache = Cache()
        self.migrating_surveys: set[MigratingSurvey] = set()

    def ship(self, cruise_cargo: [CruiseCargo]):
        try:
            for cargo in cruise_cargo:
                try:
                    self.__process_cargo(cargo)
                except RuntimeWarning as w:
                    MigrationLog.log_failed_dataset(str(w))
                    continue
            self.__process_batch_inserts()
            self.__lazy_log_survey_completion()
        except Exception as e:
            MigrationLog.log_exception(e)
            MigrationLog.log_cruise_processor_unhandled_error(cruise_cargo, str(e))
            return

    def __process_cargo(self, cargo):
        dataset_crate = cargo.dataset_crate
        survey_crate = cargo.related_survey_crate
        projects_crate = cargo.related_project_crate
        file_crates = cargo.related_file_crates

        problem_flag = False
        problem_message = ""
        MigrationLog.log_dataset_start(cargo)
        self.__add_survey_to_tracking(survey_crate)

        with ThreadPoolExecutor(6) as thread_pool:
            future_dataset = thread_pool.submit(self.__process_dataset, dataset_crate)
            future_survey = thread_pool.submit(self.__process_survey, survey_crate)
            future_scientists = thread_pool.submit(self.__process_scientists, dataset_crate.dataset_scientists)
            future_platforms = thread_pool.submit(self.__process_platforms, dataset_crate.dataset_platforms)
            future_sources = thread_pool.submit(self.__process_sources, dataset_crate.dataset_sources)
            future_instruments = thread_pool.submit(self.__process_instruments, dataset_crate.dataset_instruments)
            future_project = thread_pool.submit(self.__process_project, projects_crate)

            dataset = future_dataset.result()
            survey = future_survey.result()
            scientists = future_scientists.result()
            sources = future_sources.result()
            platforms = future_platforms.result()
            instruments = future_instruments.result()
            project = future_project.result()

        self.__validate_dataset_entry(dataset, survey, scientists, sources, platforms, instruments, project)

        self.survey_parameters = self.__package_parameters(survey.id, survey_crate.survey_parameters)
        self.dataset_parameters.extend(self.__package_parameters(dataset.id, dataset_crate.dataset_parameters))
        self.dataset_survey_mappings.extend(self.__package_mappings(dataset.id, [survey.id]))
        self.dataset_platform_mappings.extend(self.__package_mappings(dataset.id, self.__get_entity_ids(platforms)))
        self.dataset_scientist_mappings.extend(self.__package_mappings(dataset.id, self.__get_entity_ids(scientists)))
        self.dataset_source_mappings.extend(self.__package_mappings(dataset.id, self.__get_entity_ids(sources)))
        self.dataset_instrument_mappings.extend(self.__package_mappings(dataset.id, self.__get_entity_ids(instruments)))
        if project:
            self.dataset_project_mappings.extend(self.__package_mappings(dataset.id, [project.id]))

        for crate in file_crates:
            crate.file.dataset_id = dataset.id

        unique_access_paths = set()
        for crate in file_crates:
            for access_path in crate.file_access_paths:
                unique_access_paths.add(access_path)

        with ThreadPoolExecutor(len(unique_access_paths)) as thread_pool:
            thread_pool.map(self.__process_access_path, unique_access_paths)
            thread_pool.shutdown(wait=True)

        with ThreadPoolExecutor(MigrationProperties.run_parameters.file_processing_thread_count) as thread_pool:
            updated_crates_iterator = thread_pool.map(self.__process_file_crate, file_crates)
            thread_pool.shutdown(wait=True)

        updated_file_crates = strip_none(list(updated_crates_iterator))
        problem_flag, problem_message = self.__validate_dataset_file_entry(len(updated_file_crates), len(file_crates), dataset.name, problem_flag, problem_message)

        for file_crate in updated_file_crates:
            self.file_parameters.extend(self.__package_parameters(file_crate.cruise_file_id, file_crate.file_parameters))
            for acc_path in file_crate.file_access_paths:
                self.file_access_path_mappings.append(
                    (
                        file_crate.cruise_file_id,
                        self.access_path_cache.request(
                            AccessPath(path=acc_path.path, path_type=acc_path.path_type),
                            (lambda acc_path1, acc_path2: acc_path1.path == acc_path2.path and acc_path1.path_type == acc_path2.path_type)
                        ).id
                    )
                )
        inserted_datasets = 1
        inserted_files = len(updated_file_crates)
        expected_file_insertions = len(file_crates)

        MigrationReport.add_migrated_dataset(cargo)
        MigrationLog.log_migrated_dataset(cargo, inserted_files, expected_file_insertions)

        self.__update_survey_tracking(problem_flag, problem_message, survey_crate, inserted_datasets, inserted_files, expected_file_insertions)

    def __process_dataset(self, dataset_crate: CruiseDatasetCrate):
        return self.dataset_service.save_new_dataset(dataset_crate.dataset)

    def __process_survey(self, survey_crate: CruiseSurveyCrate) -> Survey:
        survey = CruiseProcessor.survey_cache.request(
            Survey(name=survey_crate.cruise_survey.survey_name),
            (lambda survey1, survey2: survey1.name == survey2.name)
        )
        if not survey:
            MigrationLog.log_survey_start(survey_crate)
            survey = self.survey_service.get_new_or_existing_survey(survey_crate.cruise_survey)
            if survey is not None:
                CruiseProcessor.survey_cache.update(survey)

        return survey

    def __process_platforms(self, dataset_platforms: [CruisePlatform]):
        platforms = []
        if dataset_platforms:
            for platform in dataset_platforms:
                cached_platform = CruiseProcessor.platform_cache.request(
                    Platform(internal_name=platform.internal_name),
                    (lambda platform1, platform2: platform1.internal_name == platform2.internal_name)
                )
                if not cached_platform:
                    db_platform = self.platform_service.get_new_or_existing_platform(platform)
                    platforms.append(db_platform)
                    if db_platform is not None:
                        CruiseProcessor.platform_cache.update(db_platform)
                else:
                    platforms.append(cached_platform)

        return platforms

    def __process_scientists(self, dataset_scientists: [CruisePeopleAndSources]):
        scientists = []
        if dataset_scientists:
            for scientist in dataset_scientists:
                cached_scientist = CruiseProcessor.scientist_cache.request(
                    Contact(name=scientist.name, organization=scientist.organization),
                    (lambda scientist1, scientist2: scientist1.name == scientist2.name and scientist1.organization == scientist2.organization)
                )
                if not cached_scientist:
                    db_scientist = self.contact_service.get_new_or_existing_scientist(scientist)
                    scientists.append(db_scientist)
                    if db_scientist is not None:
                        CruiseProcessor.scientist_cache.update(db_scientist)
                else:
                    scientists.append(cached_scientist)

        return scientists

    def __process_sources(self, dataset_sources: [CruisePeopleAndSources]):
        sources = []
        if dataset_sources:
            for source in dataset_sources:
                cached_source = CruiseProcessor.source_cache.request(
                  Contact(organization=source.organization),
                  (lambda source1, source2: source1.organization == source2.organization)
                )
                if not cached_source:
                    db_source = self.contact_service.get_new_or_existing_source(source)
                    sources.append(db_source)
                    if db_source is not None:
                        CruiseProcessor.source_cache.update(db_source)
                else:
                    sources.append(cached_source)

        return sources

    def __process_instruments(self, dataset_instruments: [CruiseInstrument]):
        instruments = []
        if dataset_instruments:
            for instrument in dataset_instruments:
                cached_instrument = CruiseProcessor.instrument_cache.request(
                  Instrument(name=instrument.instrument_name),
                  (lambda instrument1, instrument2: instrument1.name == instrument2.name)
                )
                if not cached_instrument:
                    db_instrument = self.instrument_service.get_new_or_existing_instrument(instrument)
                    instruments.append(db_instrument)
                    if db_instrument is not None:
                        CruiseProcessor.instrument_cache.update(db_instrument)
                else:
                    instruments.append(cached_instrument)

        return instruments

    def __process_project(self, project_crate: CruiseProjectCrate):
        project = project_crate.project
        return self.project_service.get_new_or_existing_project(project) if project else None

    def __process_access_path(self, access_path: CruiseAccessPath):
        cached_access_path = self.access_path_cache.request(
          AccessPath(path=access_path.path),
          (lambda path1, path2: path1.path == path2.path)
        )
        if not cached_access_path:
            db_access_path = self.access_path_service.get_new_or_existing_access_path(access_path)
            if db_access_path is not None:
                self.access_path_cache.update(db_access_path)

    def __process_file_crate(self, file_crate: CruiseFileCrate) -> Optional[CruiseFileCrate]:
        try:
            file = self.file_service.save_new_file(file_crate.file)
        except Exception as e:
            MigrationLog.log_failed_file_migration(file_crate.survey_name, file_crate.file, e)
            MigrationLog.log_exception(e)
            return None
        file_crate.cruise_file_id = file.id
        return file_crate

    def __package_parameters(self, id, parameters):
        return [self.__package_parameter_for_bulk_insertion(foreign_key_id=id, parameter=parameter) for parameter in parameters]

    @staticmethod
    def __package_parameter_for_bulk_insertion(foreign_key_id, parameter):
        data = (parameter.id, parameter.parameter_detail_id, foreign_key_id, str(parameter.value), parameter.xml, parameter.json, datetime.datetime.now(), parameter.last_updated_by)
        return data

    @staticmethod
    def __package_mappings(join_id_single, join_id_many):
        return [(join_id_single, get_joined) for get_joined in join_id_many]

    @staticmethod
    def __get_entity_ids(entities: [Entity]):
        return [entity.id for entity in entities]

    def __process_batch_inserts(self):
        with ThreadPoolExecutor(10) as thread_pool:
            thread_pool.submit(self.__batch_insert_survey_parameters, self.survey_parameters)
            thread_pool.submit(self.__batch_insert_dataset_parameters, self.dataset_parameters)
            thread_pool.submit(self.__batch_insert_dataset_survey_mappings, self.dataset_survey_mappings)
            thread_pool.submit(self.__batch_insert_dataset_scientist_mappings, self.dataset_scientist_mappings)
            thread_pool.submit(self.__batch_insert_dataset_source_mappings, self.dataset_source_mappings)
            thread_pool.submit(self.__batch_insert_dataset_platform_mappings, self.dataset_platform_mappings)
            thread_pool.submit(self.__batch_insert_dataset_project_mappings, self.dataset_project_mappings)
            thread_pool.submit(self.__batch_insert_dataset_instrument_mappings, self.dataset_instrument_mappings)
            thread_pool.submit(self.__batch_insert_file_parameters, self.file_parameters)
            thread_pool.submit(self.__batch_insert_file_access_path_mappings, self.file_access_path_mappings)

            thread_pool.shutdown(wait=True)

    @staticmethod
    def __segment(seq):
        max_size = MigrationProperties.run_parameters.batch_insertion_size
        return (seq[pos:pos + max_size] for pos in range(0, len(seq), max_size))

    def __batch_insert_survey_parameters(self, parameter_data):
        for chunk in self.__segment(parameter_data):
            self.batch_service.batch_insert_survey_parameters(chunk)

    def __batch_insert_dataset_parameters(self, parameter_data):
        for chunk in self.__segment(parameter_data):
            self.batch_service.batch_insert_dataset_parameters(chunk)

    def __batch_insert_file_parameters(self, parameter_data):
        for chunk in self.__segment(parameter_data):
            self.batch_service.batch_insert_file_parameters(chunk)

    def __batch_insert_dataset_survey_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_survey_mappings(chunk)

    def __batch_insert_dataset_scientist_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_scientist_mappings(chunk)

    def __batch_insert_dataset_source_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_source_mappings(chunk)

    def __batch_insert_dataset_platform_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_platform_mappings(chunk)

    def __batch_insert_dataset_project_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_project_mappings(chunk)

    def __batch_insert_dataset_instrument_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_dataset_instrument_mappings(chunk)

    def __batch_insert_file_access_path_mappings(self, mapping_data):
        for chunk in self.__segment(mapping_data):
            self.batch_service.batch_insert_file_access_path_mappings(chunk)

    def __update_survey_tracking(self, problem_flag: bool, problem_message: str, survey_crate: CruiseSurveyCrate, num_datasets: int, num_actual_files: int, num_expected_files: int):
        survey_name = survey_crate.cruise_survey.survey_name
        tracked_survey_set = self.migrating_surveys
        for survey in tracked_survey_set:
            if survey.survey_name == survey_name:
                survey.update(problem_flag, problem_message, num_datasets, num_actual_files, num_expected_files)

    def __add_survey_to_tracking(self, survey_crate):
        self.migrating_surveys.add(MigratingSurvey(survey_crate))

    def __lazy_log_survey_completion(self):
        tracked_survey_set = self.migrating_surveys
        for survey in tracked_survey_set:
            survey_name = survey.survey_name
            flag = survey.problem_identified
            message = survey.problem_message

            MigrationReport.add_migrated_survey(survey_name, flag, message)
            MigrationLog.log_migrated_survey(survey, flag, message)

    @staticmethod
    def __validate_dataset_file_entry(actual: int, expected_files_length: int, dataset_name: str, flag: bool, message: str) -> Tuple[bool, str]:
        if actual < expected_files_length:
            flag = True
            message = f"Some or all files failed insertion for dataset {dataset_name}; " + message
        return flag, message

    def __validate_dataset_entry(self, dataset: Dataset, survey, scientists, sources, platforms, instruments, project):
        valid = True
        if dataset is None:
            MigrationLog.log_failed_dataset("dataset insertion failed, skipping migration of related tables and files.")
            valid = False
        if survey is None:
            self.__fail_dataset(dataset, "survey")
            valid = False
        for scientist in scientists:
            if scientist is None:
                self.__fail_dataset(dataset, "scientist")
                valid = False
        for source in sources:
            if source is None:
                self.__fail_dataset(dataset, "source")
                valid = False
        for platform in platforms:
            if platform is None:
                self.__fail_dataset(dataset, "platform")
                valid = False
        for instrument in instruments:
            if instrument is None:
                self.__fail_dataset(dataset, "instrument")
                valid = False
        if project is None:
            valid = True  # project not required
        if not valid:
            raise RuntimeWarning("Issue found with dataset or dataset related tables.")

    def __fail_dataset(self, dataset, issue_context):
        message = f"dataset insertion failed due to missing record in related {issue_context} table"
        try:
            self.dataset_service.delete_dataset(dataset)
            MigrationLog.log_failed_dataset(message)
        except:
            try:
                message = message + f"; ERROR while attempting to cleanup dataset {dataset.name}"
                MigrationLog.log_failed_dataset(message)
            except:
                message = message + f"; ERROR while attempting to cleanup dataset."
                MigrationLog.log_failed_dataset(message)
