from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey
from src.mb_cruise_migration.models.mb.mb_survey_reference import SurveyReference
from src.mb_cruise_migration.models.mb.mb_mbinfo_file_tsql import MbInfo
from src.mb_cruise_migration.models.mb.mb_ngdcid_and_file import MbFile


class MbSurveyCrate(object):
    def __init__(self, survey, survey_reference, shape):
        self.mb_survey: MbSurvey = survey
        self.provider: str = self.parse_provider_from_source(survey.source)
        self.mb_survey_references: SurveyReference = survey_reference
        self.mb_survey_shape: str = shape

    @staticmethod
    def parse_provider_from_source(source: str) -> str:
        return source[source.find("(")+1:source.find(")")]


class MbFileCrate(object):
    def __init__(self, mb_file, mb_info, shape):
        self.mb_file: MbFile = mb_file
        self.mb_info: MbInfo = mb_info
        self.file_shape: str = shape
        self.non_public = None
        self.level = None
        self.dataset_type = None
        self.file_type = None
        self.platform_name = None
        self.platform_type = None

    def get_file(self):
        return self.mb_file

    def get_mbinfo(self):
        return self.mb_info


class MbCargo(object):
    """Survey-centric container for related objects being migrated"""
    def __init__(self, survey_crate, file_crates):
        self.mb_survey_crate = survey_crate
        self.related_mb_file_crates = file_crates
