import unittest

import datetime

from src.mb_cruise_migration.db.cruise_db import CruiseDb
from src.mb_cruise_migration.db.cruise_connection import CruiseConnection
from src.mb_cruise_migration.framework.consts.dataset_type_consts import DatasetTypeConsts
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.models.cruise.cruise_dataset import CruiseDataset
from src.mb_cruise_migration.models.cruise.cruise_files import CruiseFile
from src.mb_cruise_migration.services.cruise_service import FileService, DatasetService
from tests.testutils import get_file_parameters


class TestBatchInsert(unittest.TestCase):
    MigrationProperties("config_test.yaml")

    def setUp(self) -> None:
        self.tearDown()

    def tearDown(self) -> None:
        cruise_db = CruiseDb()
        cruise_db.db.query("DELETE FROM cruise.FILE_PARAMETERS")

    def test_insert_file_format_parameters(self):

        cruise_connection = CruiseConnection()

        dataset_service = DatasetService(CruiseDb())
        dataset_entity = dataset_service.save_new_dataset(
          CruiseDataset(
            other_id="NEW666",
            dataset_name="fake_dataset",
            dataset_type_name=DatasetTypeConsts.MB_RAW,
            instruments="beam machine",
            platforms="beamer",
            archive_date=datetime.datetime.now(),
            surveys="beam tour",
            projects="give me all ur beams",
            dataset_type_id=1,
          )
        )

        file_service = FileService(CruiseDb())
        file_entity = file_service.save_new_file(CruiseFile(
          file_name="jibberish",
          raw_size=9882,
          publish="Y",
          collection_date=datetime.datetime.now(),
          publish_date=datetime.datetime.now(),
          archive_date=datetime.datetime.now(),
          temp_id=None,
          gzip_size=9008,
          dataset_id=dataset_entity.id,
          version_id=1,
          type_id=1,
          format_id=32,
        ))

        query = "INSERT INTO CRUISE.FILE_PARAMETERS (FILE_PARAMETER_ID, PARAMETER_DETAIL_ID, FILE_ID, VALUE, XML, JSON, LAST_UPDATE_DATE, LAST_UPDATED_BY) VALUES (:FILE_PARAMETER_ID, :PARAMETER_DETAIL_ID, :FILE_ID, :VALUE, :XML, :JSON, :LAST_UPDATE_DATE, :LAST_UPDATED_BY)"

        data = [
          (None, 68, file_entity.id, '58', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579393), None),
          (None, 23, file_entity.id, '199', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579410), None),
          (None, 24, file_entity.id, '85968', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579420), None),
          (None, 24, file_entity.id, '85968', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579429), None),
          (None, 25, file_entity.id, '37828', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579438), None),
          (None, 27, file_entity.id, '0', None, None, datetime.datetime(2023, 2, 2, 23, 9, 48, 579448), None)
        ]

        cruise_connection.executemany(query, data)

        file_parameters = get_file_parameters()
        self.assertEqual(6, len(file_parameters))
