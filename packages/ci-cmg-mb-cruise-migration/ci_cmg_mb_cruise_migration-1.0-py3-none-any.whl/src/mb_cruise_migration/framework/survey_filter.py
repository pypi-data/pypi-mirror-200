from src.mb_cruise_migration.framework.consts.survey_blacklist import SurveyBlacklist
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.logging.migration_report import MigrationReport
from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey


class SurveyFilter(object):
    @classmethod
    def filter(cls, surveys: [MbSurvey]):
        return [survey for survey in surveys if not cls.__survey_is_blacklisted(survey)]

    @classmethod
    def __survey_is_blacklisted(cls, survey: MbSurvey) -> bool:
        blacklisted = survey.survey_name in SurveyBlacklist.BLACKLIST
        if blacklisted:
            MigrationReport.add_skipped_survey(survey.survey_name)
            MigrationLog.log_skipped_survey(survey.survey_name, "survey was blacklisted for this migration run.")
        return blacklisted
