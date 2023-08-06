from src.mb_cruise_migration.db.cruise_db import CruiseDb
from src.mb_cruise_migration.framework.consts.survey_blacklist import SurveyBlacklist
from src.mb_cruise_migration.framework.resolvers.dataset_type_resolver import DTLookup
from src.mb_cruise_migration.framework.resolvers.platform_designator_resolver import DesignatorLookup
from src.mb_cruise_migration.framework.resolvers.file_format_resolver import FFLookup
from src.mb_cruise_migration.framework.resolvers.file_type_resolver import FTLookup
from src.mb_cruise_migration.framework.consts.parameter_detail_consts import PDLookup
from src.mb_cruise_migration.framework.resolvers.version_description_resolver import VDLookup
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.services.cruise_service import FileFormatService, FileTypeService, \
    DatasetTypeService, VersionDescriptionService, ParameterDetailService, PlatformService
from src.mb_cruise_migration.services.mb_service import MbService


class ConstInitializer(object):

    @classmethod
    def initialize_consts(cls):
        MigrationLog.log.info(f"Initializing const values into memory.")
        db = CruiseDb(pooled=False)
        MigrationLog.log.info(f"Loading file formats...")
        cls.__initialize_file_formats(db)
        MigrationLog.log.info(f"Loading file types...")
        cls.__initialize_cruise_file_types(db)
        MigrationLog.log.info(f"Loading dataset types...")
        cls.__initialize_cruise_dataset_types(db)
        MigrationLog.log.info(f"Loading version descriptions...")
        cls.__initialize_cruise_version_descriptions(db)
        MigrationLog.log.info(f"Loading parameter details...")
        cls.__initialize_cruise_parameter_details(db)
        MigrationLog.log.info(f"Loading platform designator reference...")
        cls.__initialize_cruise_designator_reference(db)
        MigrationLog.log.info(f"Loading survey blacklist from config...")
        cls.__initialize_mb_survey_blacklist()

    @staticmethod
    def __initialize_file_formats(db):
        file_format_service = FileFormatService(db)
        cruise_file_formats = file_format_service.get_all_file_formats()
        FFLookup.set_id_lookup(cruise_file_formats)

        mb_service = MbService()
        mb_file_formats = mb_service.get_format_ids()
        FFLookup.set_name_lookup(mb_file_formats)

        FFLookup.validate()

    @staticmethod
    def __initialize_cruise_file_types(db):
        file_type_service = FileTypeService(db)
        file_types = file_type_service.get_all_file_types()
        FTLookup.set_lookup(file_types)
        FTLookup.validate()

    @staticmethod
    def __initialize_cruise_dataset_types(db):
        dataset_type_service = DatasetTypeService(db)
        dataset_types = dataset_type_service.get_all_dataset_types()
        DTLookup.set_lookup(dataset_types)
        DTLookup.validate()

    @staticmethod
    def __initialize_cruise_version_descriptions(db):
        version_description_service = VersionDescriptionService(db)
        version_descriptions = version_description_service.get_all_version_descriptions()
        VDLookup.set_lookups(version_descriptions)
        VDLookup.validate()

    @staticmethod
    def __initialize_cruise_parameter_details(db):
        parameter_detail_service = ParameterDetailService(db)
        parameter_details = parameter_detail_service.get_all_parameter_details()
        PDLookup.set_lookup(parameter_details)
        PDLookup.validate(parameter_detail_service)

    @staticmethod
    def __initialize_cruise_designator_reference(db):
        platform_service = PlatformService(db)
        platforms = platform_service.get_all_platforms()
        DesignatorLookup.set_lookup(platforms)

    @staticmethod
    def __initialize_mb_survey_blacklist():
        SurveyBlacklist()
