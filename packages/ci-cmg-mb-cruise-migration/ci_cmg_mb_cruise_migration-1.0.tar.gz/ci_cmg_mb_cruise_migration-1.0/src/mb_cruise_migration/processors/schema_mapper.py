import os

from src.mb_cruise_migration.framework.consts.dataset_type_consts import DatasetTypeConsts
from src.mb_cruise_migration.framework.consts.file_label_consts import FileLabels
from src.mb_cruise_migration.framework.resolvers.dataset_type_resolver import DTLookup
from src.mb_cruise_migration.framework.resolvers.file_format_resolver import FFLookup
from src.mb_cruise_migration.framework.resolvers.file_type_resolver import FTLookup
from src.mb_cruise_migration.framework.resolvers.version_description_resolver import VDLookup
from src.mb_cruise_migration.models.cruise.cruise_dataset import CruiseDataset
from src.mb_cruise_migration.framework.consts.parameter_detail_consts import ParameterDetailConsts, PDLookup
from src.mb_cruise_migration.models.cruise.cruise_access_path import CruiseAccessPath
from src.mb_cruise_migration.models.cruise.cruise_files import CruiseFile
from src.mb_cruise_migration.models.cruise.cruise_instruments import CruiseInstrument
from src.mb_cruise_migration.models.cruise.cruise_parameter import CruiseProjectParameter, CruiseDatasetParameter, CruiseSurveyParameter, CruiseFileParameter
from src.mb_cruise_migration.models.cruise.cruise_people_and_sources import CruisePeopleAndSources
from src.mb_cruise_migration.models.cruise.cruise_platforms import CruisePlatform
from src.mb_cruise_migration.models.cruise.cruise_projects import CruiseProject
from src.mb_cruise_migration.models.cruise.cruise_shape import CruiseShape
from src.mb_cruise_migration.models.cruise.cruise_surveys import CruiseSurvey
from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseSurveyCrate, CruiseProjectCrate, CruiseFileCrate
from src.mb_cruise_migration.models.intermediary.prefab import Prefab
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbFileCrate, MbSurveyCrate
from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey
from src.mb_cruise_migration.models.mb.mb_survey_reference import SurveyReference


class SchemaMapper(object):

    @staticmethod
    def load_dataset(prefab: Prefab) -> CruiseDataset:
        return CruiseDataset(
            other_id=prefab.other_id,
            dataset_name=prefab.dataset_name,
            dataset_type_name=prefab.dataset_type_name,
            instruments=prefab.instrument,
            platforms=prefab.platform,
            archive_date=prefab.archive_date,
            surveys=prefab.survey,
            projects=prefab.project,
            dataset_type_id=DTLookup.get_id(prefab.dataset_type_name),
        )

    @staticmethod
    def load_dataset_parameters(mb_survey: MbSurvey, survey_reference: SurveyReference) -> [CruiseDatasetParameter]:

        dataset_parameters = []

        if mb_survey.modify_date_data is not None:
            parameter = ParameterDetailConsts.MODIFY_DATE_DATA
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.modify_date_data, xml=None, json=None)
            )  # MB.SURVEY.MODIFY_DATE_DATA

        if mb_survey.modify_date_metadata is not None:
            parameter = ParameterDetailConsts.MODIFY_DATE_METADATA
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.modify_date_metadata, xml=None, json=None)
            )  # MB.SURVEY.MODIFY_DATE_METADATA

        if mb_survey.extract_metadata is not None:
            parameter = ParameterDetailConsts.EXTRACT_METADATA
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.extract_metadata, xml=None, json=None)
            )  # MB.SURVEY.EXTRACT_METADATA

        if mb_survey.publish is not None:
            parameter = ParameterDetailConsts.PUBLISH
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.publish, xml=None, json=None)
            )  # MB.SURVEY.PUBLISH

        if mb_survey.previous_state is not None:
            parameter = ParameterDetailConsts.PREVIOUS_STATE
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.previous_state, xml=None, json=None)
            )  # MB.SURVEY.PREVIOUS_STATE

        if survey_reference and survey_reference.download_url is not None:
            parameter = ParameterDetailConsts.DOWNLOAD_URL
            detail_id = PDLookup.get_id(parameter)
            dataset_parameters.append(
                CruiseDatasetParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=survey_reference.download_url, xml=None, json=None)
            )  # MB.SURVEY_REFERENCE.DOWNLOAD_URL

        return dataset_parameters

    @staticmethod
    def load_platforms(mb_survey: MbSurvey, prefab: Prefab) -> [CruisePlatform]:
        internal_name = prefab.datafile_path_platform_name  # derived from file data_file path.
        platform_type = prefab.datafile_path_platform_type  # derived from file data_file path.
        docucomp_uuid = None  # will be populated in some already existing platform records upon insertion
        long_name = mb_survey.ship_name  # MB.SURVEY.SHIP_NAME
        designator = prefab.platform_designator  # derived from already migrated platforms. Nullable.
        platform_name = mb_survey.ship_name  # MB.SURVEY.SHIP_NAME

        platform = CruisePlatform(
            internal_name=internal_name,
            platform_type=platform_type,
            docucomp_uuid=docucomp_uuid,
            long_name=long_name,
            designator=designator,
            platform_name=platform_name
        )
        return [platform]

    @staticmethod
    def load_scientists(mb_survey: MbSurvey) -> [CruisePeopleAndSources]:
        scientists = []
        chief_scientist = mb_survey.chief_scientist
        if chief_scientist:
            found_scientists = mb_survey.chief_scientist.split('; ')
            for scientist in found_scientists:
                names = scientist.split(', ')
                if len(names) == 2:
                    first = names[1]
                    last = names[0]
                    name = (first + " " + last)
                elif len(names) == 1:
                    first = names[0]
                    last = None
                    name = first
                else:
                    raise ValueError(f"Unexpected chief scientist field value in survey {mb_survey.survey_name}.")
                scientists.append(
                    CruisePeopleAndSources(
                        first=first,
                        last=last,
                        name=name,
                        organization=mb_survey.chief_sci_organization
                    )
                )
        return scientists

    @staticmethod
    def load_sources(mb_survey: MbSurvey) -> [CruisePeopleAndSources]:
        """in practice will be a singleton list"""
        source = CruisePeopleAndSources(organization=mb_survey.source)  # MB.SURVEY.SOURCE
        return [source]

    @staticmethod
    def load_instruments(mb_survey: MbSurvey, prefab: Prefab) -> [CruiseInstrument]:
        """in practice will be a singleton list"""

        if not DatasetTypeConsts.dataset_has_associated_instrument(prefab.dataset_type_name):
            return []

        instrument_name = prefab.instrument  # derived from MB.SURVEY.INSTRUMENT
        docucomp_uuid = None  # will be populated in some already existing instrument records upon insertion
        long_name = mb_survey.instrument  # MB.SURVEY.INSTRUMENT

        instrument = CruiseInstrument(
            instrument_name=instrument_name,
            docucomp_uuid=docucomp_uuid,
            long_name=long_name
        )

        return [instrument]

    @staticmethod
    def load_survey_crate(survey_crate: MbSurveyCrate) -> CruiseSurveyCrate:

        mb_survey = survey_crate.mb_survey
        mb_survey_reference = survey_crate.mb_survey_references
        mb_survey_shape = survey_crate.mb_survey_shape

        survey_crate = CruiseSurveyCrate()
        survey_crate.cruise_survey = SchemaMapper.load_cruise_survey(mb_survey)
        survey_crate.survey_parameters = SchemaMapper.load_cruise_survey_parameters(mb_survey, mb_survey_reference)
        survey_crate.survey_shape = SchemaMapper.load_cruise_survey_shape(mb_survey_shape)
        return survey_crate

    @staticmethod
    def load_project_crate(mb_survey: MbSurvey) -> CruiseProjectCrate:
        project_crate = CruiseProjectCrate()
        project_crate.project = SchemaMapper.load_cruise_project(mb_survey)
        project_crate.project_parameters = SchemaMapper.load_cruise_project_parameters()
        return project_crate

    @staticmethod
    def load_file_crates(files_context: [MbFileCrate], prefab: Prefab) -> [CruiseFileCrate]:
        cruise_files_crates = [SchemaMapper.load_cruise_file_crate(file, prefab) for file in files_context]
        return cruise_files_crates

    @staticmethod
    def load_cruise_survey(mb_survey: MbSurvey) -> CruiseSurvey:
        start_time = mb_survey.start_time.strftime('%Y-%m-%dT%H:%M:%S') if mb_survey.start_time else None
        end_time = mb_survey.end_time.strftime('%Y-%m-%dT%H:%M:%S') if mb_survey.end_time else None  # previously '%d-%b-%y'

        survey_name = mb_survey.survey_name        # MB.SURVEY.SURVEY_NAME
        parent = None                              # N/A
        platform_name = mb_survey.ship_name        # MB.SURVEY.SHIP_NAME
        start_date = start_time                    # MB.SURVEY.START_TIME
        end_date = end_time                        # MB.SURVEY.END_TIME-
        departure_port = mb_survey.departure_port  # MB.SURVEY.DEPARTURE_PORT
        arrival_port = mb_survey.arrival_port      # MB.SURVEY.ARRIVAL_PORT

        return CruiseSurvey(
            survey_name=survey_name,
            parent=parent,
            platform_name=platform_name,
            start_date=start_date,
            end_date=end_date,
            departure_port=departure_port,
            arrival_port=arrival_port
        )

    @staticmethod
    def load_cruise_survey_parameters(mb_survey: MbSurvey, mb_survey_reference: SurveyReference) -> [CruiseSurveyParameter]:
        survey_parameters = []

        if mb_survey.nav1 is not None:
            parameter = ParameterDetailConsts.NAV1
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.nav1, xml=None, json=None)
            )  # MB.SURVEY.NAV1

        if mb_survey.nav2 is not None:
            parameter = ParameterDetailConsts.NAV2
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.nav2, xml=None, json=None)
            )  # MB.SURVEY.NAV2

        if mb_survey.horizontal_datum is not None:
            parameter = ParameterDetailConsts.HORIZONTAL_DATUM
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.horizontal_datum, xml=None, json=None)
            )  # MB.SURVEY.HORIZONTAL_DATUM

        if mb_survey.vertical_datum is not None:
            parameter = ParameterDetailConsts.VERTICAL_DATUM
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.vertical_datum, xml=None, json=None)
            )  # MB.SURVEY.VERTICAL_DATUM

        if mb_survey.tide_correction is not None:
            parameter = ParameterDetailConsts.TIDE_CORRECTION
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.tide_correction, xml=None, json=None)
            )  # MB.SURVEY.TIDE_CORRECTION

        if mb_survey.sound_velocity is not None:
            parameter = ParameterDetailConsts.SOUND_VELOCITY
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.sound_velocity, xml=None, json=None)
            )  # MB.SURVEY.SOUND_VELOCITY

        if mb_survey.comments is not None:
            parameter = ParameterDetailConsts.COMMENTS
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.comments, xml=None, json=None)
            )  # MB.SURVEY.COMMENTS

        if mb_survey.previous_state is not None:
            parameter = ParameterDetailConsts.PREVIOUS_STATE
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.previous_state, xml=None, json=None)
            )  # MB.SURVEY.PREVIOUS_STATE

        if mb_survey.proprietary is not None:
            parameter = ParameterDetailConsts.PROPRIETARY
            detail_id = PDLookup.get_id(parameter)
            survey_parameters.append(
                CruiseSurveyParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_survey.proprietary, xml=None, json=None)
            )  # MB.SURVEY.PROPRIETARY

        return survey_parameters

    @staticmethod
    def load_cruise_survey_shape(survey_shape) -> CruiseShape:

        shape_type = "survey"
        geom_type = "line"
        shape = survey_shape

        return CruiseShape(shape_type=shape_type, geom_type=geom_type, shape=shape)

    @staticmethod
    def load_cruise_project(mb_survey: MbSurvey) -> [CruiseProject]:
        """in practice will be a singleton list"""
        project_name = mb_survey.project_name

        return CruiseProject(project_name=mb_survey.project_name) if project_name else None  # MB.SURVEY.PROJECT_NAME

    @staticmethod
    def load_cruise_project_parameters() -> [CruiseProjectParameter]:
        """No known project parameters exist for current data holdings; nothing will be migrated."""
        return []

    @staticmethod
    def load_cruise_file_crate(file_crate: MbFileCrate, prefab: Prefab) -> CruiseFileCrate:
        crate = CruiseFileCrate()
        crate.survey_name = prefab.survey
        crate.file = SchemaMapper.load_cruise_file(file_crate, prefab)
        crate.file_access_paths = SchemaMapper.load_cruise_access_paths(file_crate.mb_file.data_file, file_crate.mb_file.archive_path)
        crate.file_parameters = SchemaMapper.load_cruise_file_parameters(file_crate)
        if file_crate.file_shape is not None:
            crate.file_shape = SchemaMapper.load_cruise_file_shape(file_crate.file_shape)

        return crate

    @staticmethod
    def load_cruise_file(file_crate: MbFileCrate, prefab: Prefab) -> CruiseFile:
        mb_file = file_crate.mb_file
        file_type = prefab.files_type  # Derived: dataset type is derived from the data_file paths of files it contains, so file types of files within dataset are determined at dataset creation

        file_name = mb_file.data_file.split("/")[-1]  # derived from MB.NGDCID_AND_FILE.DATA_FILE
        raw_size = mb_file.filesize  # MB.NGDCID_AND_FILE.FILESIZE
        publish = "Y" if mb_file.publish.upper() == "yes".upper() else "N"  # derived directly from MB.NGDCID_AND_FILE.PUBLISH
        collection_date = mb_file.entry_date  # MB.NGDCID_AND_FILE.ENTRY_DATE
        # collection_date = file_crate.mb_info.start_time.strftime('%d-%b-%y %H:%M:%S') if file_crate.mb_info and file_crate.mb_info.start_time else None
        publish_date = mb_file.process_date  # MB.NGDCID_AND_FILE.PROCESS_DATE
        archive_date = mb_file.process_date  # MB.NGDCID_AND_FILE.PROCESS_DATE
        temp_id = None
        gzip_size = mb_file.filesize_gzip  # MB.NGDCID_AND_FILE.FILESIZE_GZIP
        type_id = FTLookup.get_id(file_type)
        format_id = FFLookup.get_id(FFLookup.get_name(mb_file.format_id))  # get format name from mb format id? mb_info.mbio_format_id

        version = None
        if file_crate.mb_file.label == FileLabels.STANDARD:
            version = mb_file.parsed_file.identify_version_in_path()
        version_id = VDLookup.get_id(file_type, version)

        return CruiseFile(
            file_name=file_name,
            raw_size=raw_size,
            publish=publish,
            collection_date=collection_date,
            publish_date=publish_date,
            archive_date=archive_date,
            temp_id=temp_id,
            gzip_size=gzip_size,
            version_id=version_id,
            type_id=type_id,
            format_id=format_id,
        )

    @staticmethod
    def load_cruise_file_parameters(file_crate: MbFileCrate) -> [CruiseFileParameter]:
        file_parameters = []
        if file_crate.mb_info is None:
            return file_parameters
        mb_info = file_crate.mb_info

        if mb_info.mbio_format_id is not None:
            parameter = ParameterDetailConsts.MBIO_FORMAT_ID
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.mbio_format_id, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MBIO_FORMAT_ID

        if mb_info.record_count is not None:
            parameter = ParameterDetailConsts.MB_RECORD_COUNT
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.record_count, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.RECORD_COUNT

        if mb_info.bathy_beams is not None:
            parameter = ParameterDetailConsts.MB_BATHY_BEAMS
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.bathy_beams, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.BATHY_BEAMS

        if mb_info.bathy_beams is not None:
            parameter = ParameterDetailConsts.MB_BATHY_BEAMS
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.bathy_beams, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.BATHY_BEAMS

        if mb_info.bb_good is not None:
            parameter = ParameterDetailConsts.MB_GOOD_BATH_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.bb_good, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.BB_GOOD

        if mb_info.bb_zero is not None:
            parameter = ParameterDetailConsts.MB_ZERO_BATH_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.bb_zero, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.BB_ZERO

        if mb_info.bb_flagged is not None:
            parameter = ParameterDetailConsts.MB_FLAGGED_BATH_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.bb_flagged, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.BB_FLAGGED

        if mb_info.amp_beams is not None:
            parameter = ParameterDetailConsts.MB_AMP_BEAMS
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.amp_beams, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.AMP_BEAMS

        if mb_info.ab_good is not None:
            parameter = ParameterDetailConsts.MB_GOOD_AMP_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ab_good, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.AB_GOOD

        if mb_info.ab_zero is not None:
            parameter = ParameterDetailConsts.MB_ZERO_AMP_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ab_zero, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.AB_ZERO

        if mb_info.ab_flagged is not None:
            parameter = ParameterDetailConsts.MB_FLAGGED_AMP_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ab_flagged, xml=None, json=None)
            )  # MBINFO_FILE_TSQL.AB_FLAGGED

        if mb_info.sidescans is not None:
            parameter = ParameterDetailConsts.MB_SIDESCANS
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.sidescans, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.SIDESCANS

        if mb_info.ss_good is not None:
            parameter = ParameterDetailConsts.MB_GOOD_SIDESCANS_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ss_good, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.SS_GOOD

        if mb_info.ss_zero is not None:
            parameter = ParameterDetailConsts.MB_ZERO_SIDESCANS_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ss_zero, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.SS_ZERO

        if mb_info.ss_flagged is not None:
            parameter = ParameterDetailConsts.MB_FLAGGED_SIDESCANS_TOTAL
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.ss_flagged, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.SS_FLAGGED

        if mb_info.total_time is not None:
            parameter = ParameterDetailConsts.MB_TOTAL_TIME_HOURS
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.total_time, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.TOTAL_TIME

        if mb_info.track_length is not None:
            parameter = ParameterDetailConsts.MB_TOTAL_TRACK_LENGTH_KM
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.track_length, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.TRACK_LENGTH

        if mb_info.avg_speed is not None:
            parameter = ParameterDetailConsts.MB_AVG_SPEED_KM_HR
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.avg_speed, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.AVG_SPEED

        if mb_info.start_time is not None:
            parameter = ParameterDetailConsts.MB_START_TIME
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_time, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_TIME

        if mb_info.start_lon is not None:
            parameter = ParameterDetailConsts.MB_START_LONGITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_lon, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_LON

        if mb_info.start_lat is not None:
            parameter = ParameterDetailConsts.MB_START_LATITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_lat, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_LAT

        if mb_info.start_depth is not None:
            parameter = ParameterDetailConsts.MB_START_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_DEPTH

        if mb_info.start_speed is not None:
            parameter = ParameterDetailConsts.MB_START_SPEED
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_speed, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_SPEED

        if mb_info.start_heading is not None:
            parameter = ParameterDetailConsts.MB_START_HEADING
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_heading, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_HEADING

        if mb_info.start_sonar_depth is not None:
            parameter = ParameterDetailConsts.MB_START_SONAR_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_sonar_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_SONAR_DEPTH

        if mb_info.start_sonar_alt is not None:
            parameter = ParameterDetailConsts.MB_START_SONAR_ALTITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.start_sonar_alt, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.START_SONAR_ALT

        if mb_info.end_time is not None:
            parameter = ParameterDetailConsts.MB_END_TIME
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_time, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_TIME

        if mb_info.end_lon is not None:
            parameter = ParameterDetailConsts.MB_END_LONGITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_lon, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_LON

        if mb_info.end_lat is not None:
            parameter = ParameterDetailConsts.MB_END_LATITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_lat, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_LAT

        if mb_info.end_depth is not None:
            parameter = ParameterDetailConsts.MB_END_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_DEPTH

        if mb_info.end_speed is not None:
            parameter = ParameterDetailConsts.MB_END_SPEED
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_speed, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_SPEED

        if mb_info.end_heading is not None:
            parameter = ParameterDetailConsts.MB_END_HEADING
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_heading, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_HEADING

        if mb_info.end_sonar_depth is not None:
            parameter = ParameterDetailConsts.MB_END_SONAR_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_sonar_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_SONAR_DEPTH

        if mb_info.end_sonar_alt is not None:
            parameter = ParameterDetailConsts.MB_END_SONAR_ALTITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.end_sonar_alt, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.END_SONAR_ALT

        if mb_info.min_lon is not None:
            parameter = ParameterDetailConsts.MB_MIN_LONGITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_lon, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_LON

        if mb_info.max_lon is not None:
            parameter = ParameterDetailConsts.MB_MAX_LONGITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_lon, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_LON

        if mb_info.min_lat is not None:
            parameter = ParameterDetailConsts.MB_MIN_LATITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_lat, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_LAT

        if mb_info.max_lat is not None:
            parameter = ParameterDetailConsts.MB_MAX_LATITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_lat, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_LAT

        if mb_info.min_sonar_depth is not None:
            parameter = ParameterDetailConsts.MB_MIN_SONAR_DEPTH_M
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_sonar_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_SONAR_DEPTH

        if mb_info.max_sonar_depth is not None:
            parameter = ParameterDetailConsts.MB_MAX_SONAR_DEPTH_M
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_sonar_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_SONAR_DEPTH

        if mb_info.min_sonar_alt is not None:
            parameter = ParameterDetailConsts.MB_MIN_SONAR_ALTITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_sonar_alt, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_SONAR_ALT

        if mb_info.max_sonar_alt is not None:
            parameter = ParameterDetailConsts.MB_MAX_SONAR_ALTITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_sonar_alt, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_SONAR_ALT

        if mb_info.min_depth is not None:
            parameter = ParameterDetailConsts.MB_MIN_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_DEPTH

        if mb_info.max_depth is not None:
            parameter = ParameterDetailConsts.MB_MAX_DEPTH
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_depth, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_DEPTH

        if mb_info.min_amp is not None:
            parameter = ParameterDetailConsts.MB_MIN_AMPLITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_amp, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_AMP

        if mb_info.max_amp is not None:
            parameter = ParameterDetailConsts.MB_MAX_AMPLITUDE
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_amp, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_AMP

        if mb_info.min_sidescan is not None:
            parameter = ParameterDetailConsts.MB_MIN_SIDESCAN
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.min_sidescan, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MIN_SIDESCAN

        if mb_info.max_sidescan is not None:
            parameter = ParameterDetailConsts.MB_MAX_SIDESCAN
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.max_sidescan, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.MAX_SIDESCAN

        if mb_info.objectid is not None:
            parameter = ParameterDetailConsts.MB_OBJECT_ID
            detail_id = PDLookup.get_id(parameter)
            file_parameters.append(
                CruiseFileParameter(parameter_detail_name=parameter, parameter_detail_id=detail_id, value=mb_info.objectid, xml=None, json=None)
            )  # MB.MBINFO_FILE_TSQL.OBJECTID

        return file_parameters

    @staticmethod
    def load_cruise_access_paths(data_file, archive_path) -> [CruiseAccessPath]:
        disk = CruiseAccessPath(
            path=os.path.dirname(data_file),
            path_type="Disk"
        ) if data_file else None  # MB.NGDCID_AND_FILE.DATA_FILE

        archive = CruiseAccessPath(
            path=os.path.dirname(archive_path),
            path_type="Stornext"
        ) if archive_path else None  # MB.NGDCID_AND_FILE.ARCHIVE_PATH

        return [path for path in [disk, archive] if path is not None]

    @staticmethod
    def load_cruise_file_shape(mb_survey_shape) -> CruiseShape:
        shape_type = "file"
        geom_type = "line"
        shape = mb_survey_shape

        return CruiseShape(shape_type=shape_type, geom_type=geom_type, shape=shape)
