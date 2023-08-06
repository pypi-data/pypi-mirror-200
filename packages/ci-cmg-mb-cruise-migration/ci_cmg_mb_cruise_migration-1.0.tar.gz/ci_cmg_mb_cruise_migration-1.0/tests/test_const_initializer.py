import unittest

from src.mb_cruise_migration.framework.resolvers.dataset_type_resolver import DTLookup
from src.mb_cruise_migration.framework.resolvers.file_format_resolver import FFLookup
from src.mb_cruise_migration.framework.resolvers.file_type_resolver import FTLookup
from src.mb_cruise_migration.framework.resolvers.version_description_resolver import VDLookup
from src.mb_cruise_migration.framework.consts.const_initializer import ConstInitializer
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.migration_properties import MigrationProperties


class TestConstInitializer(unittest.TestCase):
    MigrationProperties("config_test.yaml")
    MigrationLog()

    def test_cruise_const_setup(self):
        try:
            ConstInitializer.initialize_consts()

            self.assertEqual(1, DTLookup.get_id("MB RAW"))
            self.assertEqual(9, DTLookup.get_id("METADATA"))

            self.assertEqual(2, FTLookup.get_id("MB PROCESSED"))
            self.assertEqual(5, FTLookup.get_id("DOCUMENT"))

            self.assertEqual(20, FFLookup.get_id("MBF_HSLDEDMB"))
            self.assertEqual(75, FFLookup.get_id("ASCII_TEXT"))

            self.assertEqual(3, VDLookup.get_id_from_description("PRODUCT"))
            self.assertEqual(2, VDLookup.get_version_number_from_description("PROCESSED"))

        except:
            self.fail()
