import unittest

from src.mb_cruise_migration.migrator import Migrator
from src.mb_cruise_migration.processors.cruise_processor import CruiseProcessor

from tests.testutils import clean_mb_db, clean_cruise_db, reset_properties, \
    get_cruise_surveys, get_cruise_datasets, get_files, get_platforms, \
    get_instruments, get_projects, get_people_and_sources, get_access_paths, \
    get_shapes, get_survey_parameters, get_project_parameters, \
    get_dataset_parameters, get_file_parameters, get_dataset_projects, \
    get_dataset_platforms, get_dataset_instrument, get_dataset_surveys, \
    get_scientists, get_sources, get_dataset_shapes, get_survey_shapes, \
    get_file_shapes, get_file_access_paths, load_test_mb_data


class TestEndToEndIntegration(unittest.TestCase):

    def setUp(self) -> None:
        reset_properties()
        self.tearDown()

    def tearDown(self) -> None:
        self.migrator = Migrator("config_test.yaml")
        clean_mb_db()
        clean_cruise_db()
        CruiseProcessor.source_cache.clean_cache()
        CruiseProcessor.instrument_cache.clean_cache()
        CruiseProcessor.survey_cache.clean_cache()
        CruiseProcessor.scientist_cache.clean_cache()
        CruiseProcessor.platform_cache.clean_cache()
        CruiseProcessor.project_cache.clean_cache()

    def test_end_to_end_RR1808_lite(self):
        test_data_file = "RR1808_lite.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=2,
            num_datasets_with_instruments=1,
            num_instruments=1,
            num_scientists=1,
            num_files=8,
            num_mbinfo_records=2,
            num_access_paths=4,
            num_survey_params=3,
        )

    @unittest.skip("Not implemented yet.")
    def test_end_to_end_NEW1208_lite(self):
        """a.k.a HE0302"""
        test_data_file = "NEW1208_lite.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator()
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=1,
            num_datasets_with_instruments=0,
            num_instruments=1,
            num_scientists=1,
            num_files=8,
            num_mbinfo_records=2,
            num_access_paths=4,
            num_survey_params=3,
            num_dataset_platforms=0
        )

    # def test_end_to_end_RR1808_with_shapes(self):
    #     test_data_file = "RR1808_lite.sql"
    #     load_test_mb_data(test_data_file)
    #
    #     MigrationProperties("config_test.yaml")
    #     MigrationProperties.run_parameters.migrate_shapes = True
    #     MigrationLog()
    #     MigrationReport()
    #
    #     num_datasets = 2
    #     num_datasets_with_instruments = 1
    #     num_instruments = 1
    #     num_scientists = 1
    #     num_files = 8
    #     num_mbinfo_records = 2
    #     file_shapes = num_mbinfo_records
    #     num_access_paths = 4
    #     num_survey_params = 3
    #

    def test_end_to_end_RR1808(self):
        test_data_file = "RR1808.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=2,
            num_datasets_with_instruments=1,
            num_instruments=1,
            num_scientists=1,
            num_files=157,
            num_mbinfo_records=142,
            num_access_paths=4,
            num_survey_params=3,
        )

    def test_end_to_end_NEW3020(self):
        """
        AKA EX1907. OER survey that made it through the original MB ingest pipeline without issue.
        It has version1 and version2 data.  One instrument.  Products.  Metadata.  Ancillary.
        Two chief scientists in MB.SURVEY with a semicolon delimiter.  All the good things.
        """

        test_data_file = "NEW3020.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=5,
            num_datasets_with_instruments=3,
            num_instruments=1,
            num_scientists=2,
            num_files=989,
            num_mbinfo_records=811,
            num_access_paths=12,
            num_survey_params=1  # Previous_State
        )

    def test_end_to_end_NEW3549(self):
        """
        another OER survey.  Same story as the above, with an added note that the provided .gsf's were problematic during
        initial ingest due to a compatibility issue with the old version of MB-System.
        I am interested in confirming that the gsf's (v2) make it to CRUISE without issue.
        They should, since the migration script isn't using MB-System.
        """

        test_data_file = "NEW3549.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=4,
            num_instruments=1,
            num_datasets_with_instruments=2,
            num_scientists=1,
            num_files=603,  # WCD file gets filtered out
            num_mbinfo_records=240,
            num_access_paths=10,
            num_survey_params=1,  # Previous_State
            num_file_access_paths=1206  # two less due to wcd file getting filtered out
        )

    def test_end_to_end_NEW1570(self):
        """
        yet another OER survey.  We recently had to take this one from public to nonpublic due to sensitive data.
        I want to make sure it is flagged as nonpublic appropriately in cruise post-migration.
        It will be representative of several other similar ones.
        """
        test_data_file = "NEW1570.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        num_files = 450

        self.validate_structure_results(
            num_datasets=5,
            num_instruments=1,
            num_datasets_with_instruments=3,
            num_scientists=1,
            num_files=450,  # filters out WCD "file"
            num_access_paths=13,  # one less than normal due to no archive path for survey metadata
            num_survey_params=4,  # NAV1, Comments, Previous_State, Proprietary
            num_paths_per_file=1,
            num_file_access_paths=(num_files*2) - 1,  # survey metadata only has one access path, wcd file already "filtered" out of total
            num_file_parameters=1,
            num_mbinfo_records=16345,  # not all mbinfo records fully populated. 194 have 14 null values. So, 16345 file parameters instead of normal 19061
        )

    def test_end_to_end_NEW3206(self):
        """
        this one has two sources, R2R (version1) and MGDS (version2).  These should become separate datasets.
        """
        test_data_file = "NEW3206.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=3,
            num_datasets_with_instruments=2,
            num_instruments=1,
            num_scientists=1,
            num_files=103,
            num_mbinfo_records=91,
            num_access_paths=8,
            num_survey_params=3,  # NAV1, Previous_State, Proprietary
        )

    def test_end_to_end_NEW3370(self):
        """
        AKA AR52-A. two instruments.
        """
        test_data_file = "NEW3370.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=3,
            num_datasets_with_instruments=2,
            num_instruments=2,
            num_scientists=1,
            num_files=25,
            num_mbinfo_records=18,
            num_access_paths=6,
            num_survey_params=3,  # NAV1, Previous_State, Proprietary
        )

    def test_end_to_end_NEW1208(self):
        """
        AKA HE0302. ECS survey (high priority to get right).  Contains version1, version2, and version3.
        Products in both version2 and version3.  No instrument directories.
        """

        test_data_file = "NEW1208.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=5,
            num_datasets_with_instruments=3,
            num_instruments=1,
            num_scientists=1,
            num_files=522,
            num_mbinfo_records=243,
            num_access_paths=17,  # no archive path for survey metadata
            num_survey_params=3,  # NAV1, Previous_State, Proprietary
            num_file_access_paths=1043
        )

    def test_end_to_end_NEW523(self):
        """
        AKA HLY0302
        curiosity on my part.  We can discuss this one.
        Technically it's actually the same survey as HE0302 and is something we
        will clean up eventually (NOT something we need to clean up as a part of
        the migration script).  Version1 data from R2R, no instrument directory.
        """

        test_data_file = "NEW523.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=2,
            num_datasets_with_instruments=1,
            num_instruments=1,
            num_scientists=1,
            num_files=237,
            num_mbinfo_records=235,
            num_access_paths=3,  # one less due to survey metadata file (no archive path)
            num_survey_params=3,  # NAV1, Comments, Proprietary
            num_file_access_paths=473,  # one less due to survey metadata file (no archive path)
            num_dataset_parameters=5,  # "previous state" parameter is null
        )

    def test_end_to_end_NEW2176(self):
        """
        AKA CB13_01
        submission from Geological Survey of Ireland.  Files are on tape but not disk due to MB-System compatibility issues.
        Files are included in the database but don't have geometries.
        I would like to see how this one plays out in migration, but it should not require modifications.
        """

        test_data_file = "NEW2176.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=2,
            num_datasets_with_instruments=1,
            num_instruments=1,
            num_scientists=1,
            num_files=1048,
            num_mbinfo_records=0,
            num_access_paths=5,
            num_survey_params=4,  # NAV1, Horizontal_Datum, Vertical_Datum, Previous_State
            num_dataset_parameters=5,  # no download url
            num_file_access_paths=2095  # one less due to survey metadata file
        )

    def test_end_to_end_NEW3106(self):
        """
        AKA FSPT180004
        submission from Fugro, one of our regular providers.  Should be straightforward.
        One instrument, one level of processing, and one metadata record and some ancillary.
        """
        test_data_file = "NEW3106.sql"
        load_test_mb_data(test_data_file)

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        self.validate_structure_results(
            num_datasets=3,
            num_datasets_with_instruments=1,
            num_instruments=1,
            num_scientists=0,
            num_files=285,
            num_mbinfo_records=283,
            num_access_paths=6,
            num_survey_params=4,  # NAV1, Horizontal_Datum, Previous_State, Proprietary
        )

    def test_end_to_end_all_at_once(self):

        load_test_mb_data("RR1808.sql")
        load_test_mb_data("NEW3020.sql")
        load_test_mb_data("NEW3549.sql")
        load_test_mb_data("NEW1570.sql")
        load_test_mb_data("NEW3206.sql")
        load_test_mb_data("NEW3370.sql")
        load_test_mb_data("NEW1208.sql")
        load_test_mb_data("NEW523.sql")
        load_test_mb_data("NEW2176.sql")
        load_test_mb_data("NEW3106.sql")

        migrator = Migrator("config_test.yaml")
        migrator.migrate()

        surveys = get_cruise_surveys()
        datasets = get_cruise_datasets()
        files = get_files()

        with self.subTest(msg="bulk_datasets"):
            self.assertEqual(34, len(datasets))
        with self.subTest(msg="bulk_surveys"):
            self.assertEqual(10, len(surveys))
        with self.subTest(msg="bulk_files"):
            self.assertEqual(4419, len(files))

    @unittest.skip("Not implemented.")
    def test_end_to_end_leg_dataset(self):
        pass

    @unittest.skip("Not implemented.")
    def test_end_to_end_region_dataset(self):
        pass

    @unittest.skip("Not implemented.")
    def test_end_to_end_zone_dataset(self):
        pass

    @unittest.skip("Not implemented.")
    def test_end_to_end_missing_datatype_dataset(self):
        pass

    @unittest.skip("Not implemented.")
    def test_end_to_end_erroneous_dataset(self):
        # Will include a variety of type specific cases that should be fixed in db rather
        # than handled here if at all possible. This function is just a placeholder for now.
        pass

    def validate_structure_results(
            self,
            num_datasets,
            num_instruments,
            num_datasets_with_instruments,
            num_scientists,
            num_files,
            num_mbinfo_records,
            num_access_paths,
            num_survey_params,
            num_shapes=0,
            num_survey_shapes=0,
            num_dataset_shapes=0,
            num_file_shapes=0,
            num_paths_per_file=2,
            num_dataset_parameters=6,
            num_file_parameters=49,
            num_dataset_platforms=1,
            num_file_access_paths=None
            ):
        if not num_file_access_paths:
            num_file_access_paths = (num_files * num_paths_per_file)

        surveys = get_cruise_surveys()
        datasets = get_cruise_datasets()
        files = get_files()
        platforms = get_platforms()
        instruments = get_instruments()
        projects = get_projects()
        people_and_sources = get_people_and_sources()
        access_paths = get_access_paths()
        shapes = get_shapes()
        dataset_project_mappings = get_dataset_projects()
        dataset_platform_mappings = get_dataset_platforms()
        dataset_instrument_mappings = get_dataset_instrument()
        dataset_surveys_mappings = get_dataset_surveys()
        scientist_mappings = get_scientists()
        source_mappings = get_sources()
        dataset_shape_mappings = get_dataset_shapes()
        survey_shape_mappings = get_survey_shapes()
        file_shape_mappings = get_file_shapes()
        file_access_path_mappings = get_file_access_paths()
        project_params = get_project_parameters()
        survey_params = get_survey_parameters()
        dataset_params = get_dataset_parameters()
        file_params = get_file_parameters()

        with self.subTest(msg="survey"):
            self.assertEqual(1, len(surveys))
        with self.subTest(msg="datasets"):
            self.assertEqual(num_datasets, len(datasets))
        with self.subTest(msg="files"):
            self.assertEqual(num_files, len(files))
        with self.subTest(msg="platform"):
            self.assertEqual(num_dataset_platforms, len(platforms))
        with self.subTest(msg="instruments"):
            self.assertEqual(num_instruments, len(instruments))
        with self.subTest(msg="project"):
            self.assertEqual(1, len(projects))
        with self.subTest(msg="contacts"):
            self.assertEqual(num_scientists + 1, len(people_and_sources))
        with self.subTest(msg="access paths"):
            self.assertEqual(num_access_paths, len(access_paths))
        with self.subTest(msg="shapes"):
            self.assertEqual(num_shapes, len(shapes))
        with self.subTest(msg="dataset project mapping"):
            self.assertEqual(num_datasets, len(dataset_project_mappings))
        with self.subTest(msg="dataset platform mapping"):
            self.assertEqual(num_datasets * num_dataset_platforms, len(dataset_platform_mappings))
        with self.subTest(msg="dataset instrument mappings"):
            self.assertEqual(num_datasets_with_instruments, len(dataset_instrument_mappings))
        with self.subTest(msg="dataset survey mapping"):
            self.assertEqual(num_datasets, len(dataset_surveys_mappings))
        with self.subTest(msg="scientists"):
            self.assertEqual(num_datasets * num_scientists, len(scientist_mappings))
        with self.subTest(msg="source"):
            self.assertEqual(num_datasets, len(source_mappings))
        with self.subTest(msg="dataset shapes"):
            self.assertEqual(num_dataset_shapes, len(dataset_shape_mappings))
        with self.subTest(msg="survey shapes"):
            self.assertEqual(num_survey_shapes, len(survey_shape_mappings))
        with self.subTest(msg="file shapes"):
            self.assertEqual(num_file_shapes, len(file_shape_mappings))
        with self.subTest(msg="file access_path mappings"):
            self.assertEqual(num_file_access_paths, len(file_access_path_mappings))
        with self.subTest(msg="project parameters"):
            self.assertEqual(0, len(project_params))
        with self.subTest(msg="survey parameters"):
            self.assertEqual(num_survey_params, len(survey_params))
        with self.subTest(msg="dataset parameters"):
            self.assertEqual(num_datasets * num_dataset_parameters, len(dataset_params))
        with self.subTest(msg="file parameters"):
            self.assertEqual(num_mbinfo_records * num_file_parameters, len(file_params))
