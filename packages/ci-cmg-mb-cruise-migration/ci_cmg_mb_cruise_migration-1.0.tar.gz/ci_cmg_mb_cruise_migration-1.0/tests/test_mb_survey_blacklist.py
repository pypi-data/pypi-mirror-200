import unittest

from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.framework.consts.const_initializer import ConstInitializer
from src.mb_cruise_migration.processors.mb_processor import MbProcessor
from tests.testutils import load_test_mb_data, clean_mb_db


class TestSurveyBlacklist(unittest.TestCase):
    MigrationProperties("config_test.yaml")
    MigrationLog()

    def setUp(self) -> None:
        self.tearDown()

    def tearDown(self) -> None:
        clean_mb_db()

    def test_survey_blacklist(self):
        ConstInitializer.initialize_consts()
        test_data_file = "test_blacklist.sql"
        load_test_mb_data(test_data_file)

        mb_processor = MbProcessor()

        mb_cargo = mb_processor.load()
        self.assertEqual(1, len(mb_cargo))
