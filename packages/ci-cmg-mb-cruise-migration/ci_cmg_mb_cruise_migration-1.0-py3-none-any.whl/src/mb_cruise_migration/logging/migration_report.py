import logging

from src.mb_cruise_migration.framework.consts.log_level_consts import LogLevels
from src.mb_cruise_migration.logging.migration_logger import LoggerBuilder
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseCargo
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbSurveyCrate


class FailedSurvey(object):
    def __init__(self, survey, error):
        self.survey_name = survey
        self.error_message = error


class ProblemSurvey(object):
    def __init__(self, survey, message):
        self.survey_name = survey
        self.message = message


class MigrationReport(LoggerBuilder):
    report: logging.Logger = None
    start = None
    end = None
    success = True
    failure_message = None

    migrated_surveys = []
    problem_surveys: [ProblemSurvey] = []
    skipped_surveys = []
    failed_surveys: [FailedSurvey] = []

    total_migrated_datasets = 0
    total_migrated_files = 0
    total_instrument_review_files = 0

    def __init__(self):
        self.__pre_check()

        keyword = "migration_report"
        handler = self.__get_report_handler(keyword)
        formatter = self.get_report_formatter()
        super(MigrationReport, self).__init__(keyword, LogLevels.INFO, handler, formatter)

        MigrationReport.report = self.get_logger()

    @staticmethod
    def __pre_check():
        if not MigrationProperties.log_config:
            raise RuntimeError("Properties must be loaded prior to creating a logger")

    @staticmethod
    def __get_report_handler(keyword):
        log_root = MigrationProperties.log_config.log_root
        log_dir = MigrationProperties.log_config.report_path
        log_path = LoggerBuilder.create_log_file_path(log_root, log_dir, keyword)

        return logging.FileHandler(log_path, 'w')

    @staticmethod
    def get_report_formatter():
        return logging.Formatter('%(message)s')

    @staticmethod
    def add_migrated_dataset(cargo: CruiseCargo):
        MigrationReport.total_migrated_datasets += 1
        num_files = len(cargo.related_file_crates)
        MigrationReport.total_migrated_files += num_files

    @staticmethod
    def add_migrated_survey(survey_name: str, problem_flag: bool, problem_message: str):
        if problem_flag:
            MigrationReport.add_problem_survey(survey_name, problem_message)
        else:
            MigrationReport.migrated_surveys.append(survey_name)

    @staticmethod
    def add_problem_survey(survey_name: str, message: str):
        MigrationReport.problem_surveys.append(ProblemSurvey(survey_name, message))

    @staticmethod
    def add_skipped_survey(survey_name: str):
        MigrationReport.skipped_surveys.append(survey_name)

    @staticmethod
    def add_failed_survey(survey_crate: MbSurveyCrate, exception):
        message = "Failed to identify issue with survey. Survey migration was cancelled due to thrown error."
        try:
            message = str(exception)
        except UnicodeDecodeError:
            print("Failed to decode exception message.")

        MigrationReport.failed_surveys.append(FailedSurvey(survey_crate.mb_survey.survey_name, message))

    @staticmethod
    def increment_review_files_total():
        MigrationReport.total_instrument_review_files += 1

    @staticmethod
    def migration_final_report():
        logger = MigrationReport.report
        total_migrated_surveys = len(MigrationReport.migrated_surveys)
        total_failed_surveys = len(MigrationReport.failed_surveys)
        total_skipped_surveys = len(MigrationReport.skipped_surveys)
        total_problem_surveys = len(MigrationReport.problem_surveys)
        total_time = (MigrationReport.end - MigrationReport.start).total_seconds() / 60

        logger.info(f"MIGRATION COMPLETED {'SUCCESSFULLY' if MigrationReport.success else 'UNSUCCESSFULLY'}")
        if not MigrationReport.success:
            logger.info(f"\n{MigrationReport.failure_message}\n")
        logger.info(f'Elapsed time in minutes: {total_time}')
        logger.info(f"\r")

        logger.info(f'SUMMARY')
        logger.info(f"\tmigrated surveys: {total_migrated_surveys}")
        logger.info(f"\tfailed surveys: {total_failed_surveys}")
        logger.info(f"\tskipped surveys: {total_skipped_surveys}")
        logger.info(f"\tproblem surveys: {total_problem_surveys}")
        logger.info(f"\r")
        logger.info(f"\tmigrated datasets: {MigrationReport.total_migrated_datasets}")
        logger.info(f"\tmigrated files: {MigrationReport.total_migrated_files}")
        reviewable_percent = int(MigrationReport.total_instrument_review_files / MigrationReport.total_migrated_files)
        logger.info(f"\tfiles requiring instrument review: {MigrationReport.total_instrument_review_files} -- {reviewable_percent}% of total files")
        logger.info(f"\r")
        logger.info(f"\r")

        logger.info(f'BREAKDOWN')
        logger.info(f"Migrated surveys (no problems flagged):")
        migrated_surveys = MigrationReport.get_successful_surveys_without_problems()
        for survey in migrated_surveys:
            logger.info(f"\t{survey}")
        logger.info(f"\r")
        logger.info(f"Problem surveys (surveys flagged for review during migration):")
        for survey in MigrationReport.problem_surveys:
            # logger.info(f"\t{survey.survey_name}; {survey.message}")
            logger.info(f"\t{survey.survey_name}")
        logger.info(f"\r")
        logger.info(f"Skipped surveys (surveys explicitly omitted via migration config):")
        for survey in MigrationReport.skipped_surveys:
            logger.info(f"\t{survey}")
        logger.info(f"\r")
        logger.info(f"Failed surveys (migration was attempted, but an error occurred):")
        for survey in MigrationReport.failed_surveys:
            # logger.info(f"\t{survey.survey_name};\r{survey.error_message}\r")
            logger.info(f"\t{survey.survey_name}")
        logger.info(f"\r")

        print("MIGRATION COMPLETED: Elapsed time: ", total_time)

    @staticmethod
    def clean_final_report():
        logger = MigrationReport.report
        total_time = (MigrationReport.end - MigrationReport.start).total_seconds() / 60

        logger.info(f"DELETION OF MULTIBEAM DATA COMPLETED")
        logger.info(f'Elapsed time in minutes: {total_time}')
        logger.info(f"\r")

    @staticmethod
    def get_successful_surveys_without_problems():
        successful = MigrationReport.migrated_surveys
        problems = MigrationReport.problem_surveys
        problems = [problem.survey_name for problem in problems]
        if problems and successful:
            successful = [survey for survey in successful if survey not in problems]

        return successful
