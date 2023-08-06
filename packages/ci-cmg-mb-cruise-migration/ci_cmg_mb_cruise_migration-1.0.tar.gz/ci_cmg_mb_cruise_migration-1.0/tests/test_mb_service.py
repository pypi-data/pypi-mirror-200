import unittest

from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.models.mb.mb_mbinfo_file_tsql import MbInfo
from src.mb_cruise_migration.models.mb.mb_ngdcid_and_file import MbFile
from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey
from src.mb_cruise_migration.models.mb.mb_survey_reference import SurveyReference
from src.mb_cruise_migration.services.mb_service import MbService
from tests.testutils import load_test_mb_data, clean_mb_db


class TestMbService(unittest.TestCase):
    MigrationProperties("config_test.yaml")  # load app configuration from file
    MigrationLog()
    mb_service: MbService = MbService()
    test_data_file = "RR1808_lite.sql"

    def setUp(self) -> None:
        load_test_mb_data(self.test_data_file)

    def tearDown(self) -> None:
        clean_mb_db()

    def test_insert(self):
        row = {'NGDC_ID': "66666666", 'CREATED_BY': "ahab", 'DOWNLOAD_URL': "noaa.com"}
        self.mb_service.insert_row(table="SURVEY_REFERENCE", row=row)

    def test_select_table_size(self):
        clean_mb_db()
        for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]:
            row = {'NGDC_ID': "1111" + i, 'CREATED_BY': "klaus", 'DOWNLOAD_URL': "noaa.com"}
            self.mb_service.insert_row(table="SURVEY_REFERENCE", row=row)
        size = self.mb_service.get_survey_count("SURVEY_REFERENCE")
        self.assertEqual(size, 13)

    def test_survey_page_retrieval(self):
        surveys = self.mb_service.get_survey_page(0, 1)
        self.assertEqual(len(surveys), 1)
        self.assertIsInstance(surveys[0], MbSurvey)
        self.assertEqual("NEW2930", surveys[0].ngdc_id)

    def test_get_survey_refs(self):
        survey_ref = self.mb_service.get_survey_reference("NEW2930")
        self.assertIsInstance(survey_ref, SurveyReference)

    def test_get_survey_shape(self):
        shape = self.mb_service.get_survey_shape("NEW2930")
        self.assertIsNotNone(shape)

    def test_get_files(self):
        survey_files = self.mb_service.get_survey_files("NEW2930")
        self.assertEqual(len(survey_files), 8)
        self.assertIsInstance(survey_files[0], MbFile)

    def test_get_file_shape(self):
        shape = self.mb_service.get_file_shape("ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0140_20180617_101452_revelle.all.mb58.gz")
        self.assertIsNotNone(shape)

    def test_get_files_mb_info(self):
        survey_files = self.mb_service.get_survey_files("NEW2930")
        for file in survey_files:
            mbinfo = self.mb_service.get_mb_info(file.data_file)
            if mbinfo:
                self.assertIsInstance(mbinfo, MbInfo)


if __name__ == '__main__':
    unittest.main()
