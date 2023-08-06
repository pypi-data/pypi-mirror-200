import datetime
import unittest

from src.mb_cruise_migration.db.cruise_db import CruiseDb
from src.mb_cruise_migration.framework.parsed_data_file import ParsedFilePath
from src.mb_cruise_migration.framework.file_decoder import FileDecoder
from src.mb_cruise_migration.logging.migration_log import MigrationLog
from tests.testutils import clean_cruise_db
from src.mb_cruise_migration.migration_properties import MigrationProperties

from src.mb_cruise_migration.framework.resolvers.dataset_type_resolver import DatasetTypeConsts, DTLookup
from src.mb_cruise_migration.framework.consts.file_label_consts import FileLabels
from src.mb_cruise_migration.framework.consts.platform_type_consts import PlatformTypeConsts
from src.mb_cruise_migration.models.cruise.cruise_access_path import CruiseAccessPath
from src.mb_cruise_migration.models.cruise.cruise_dataset import CruiseDataset
from src.mb_cruise_migration.models.cruise.cruise_files import CruiseFile
from src.mb_cruise_migration.models.cruise.cruise_instruments import CruiseInstrument
from src.mb_cruise_migration.models.cruise.cruise_parameter import CruiseDatasetParameter, CruiseFileParameter, CruiseSurveyParameter
from src.mb_cruise_migration.models.cruise.cruise_people_and_sources import CruisePeopleAndSources
from src.mb_cruise_migration.models.cruise.cruise_platforms import CruisePlatform
from src.mb_cruise_migration.models.cruise.cruise_projects import CruiseProject
from src.mb_cruise_migration.models.cruise.cruise_shape import CruiseShape
from src.mb_cruise_migration.models.cruise.cruise_surveys import CruiseSurvey
from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseCargo
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbCargo, MbSurveyCrate, MbFileCrate
from src.mb_cruise_migration.models.mb.mb_mbinfo_file_tsql import MbInfo
from src.mb_cruise_migration.models.mb.mb_ngdcid_and_file import MbFile
from src.mb_cruise_migration.models.mb.mb_survey import MbSurvey
from src.mb_cruise_migration.models.mb.mb_survey_reference import SurveyReference
from src.mb_cruise_migration.framework.consts.const_initializer import ConstInitializer
from src.mb_cruise_migration.processors.transfer_station import TransferStation
from src.mb_cruise_migration.services.cruise_service import PlatformService


class TestStandardMapping(unittest.TestCase):

    def tearDown(self) -> None:
        clean_cruise_db()

    def test_standard(self):
        MigrationProperties("config_test.yaml")
        MigrationLog()

        # PREP DB
        platform_service = PlatformService(CruiseDb())
        platform_service.get_new_or_existing_platform(
            CruisePlatform(
                internal_name="roger_revelle",
                platform_type="ship",
                docucomp_uuid=None,
                long_name="Roger Revelle",
                designator="RR",
                platform_name=None
            )
        )

        ConstInitializer.initialize_consts()

        # SETUP MB TEST OBJECTS
        mb_survey_crate = self._create_standard_test_mb_survey_crate()
        mb_file_crates = self._create_standard_test_mb_file_crates()

        mb_crate = MbCargo(file_crates=mb_file_crates, survey_crate=mb_survey_crate)
        station = TransferStation(mb_crate)

        # TEST
        cruise_cargo = station.transfer()
        self.assertEqual(1, len(cruise_cargo))

        cargo = cruise_cargo[0]
        self.assertTrue(isinstance(cargo, CruiseCargo))

        # survey and survey related tables
        survey = cargo.related_survey_crate.cruise_survey
        self.assertTrue(isinstance(survey, CruiseSurvey))
        self.assertIsNone(survey.id)
        self.assertEqual("RR1808", survey.survey_name)
        self.assertIsNone(survey.parent)
        self.assertEqual("Roger Revelle", survey.platform_name)
        self.assertEqual("2018-06-13T00:00:00", survey.start_date)
        self.assertEqual("2018-06-17T00:00:00", survey.end_date)
        self.assertEqual("Newport, Oregon", survey.departure_port)
        self.assertEqual("Newport, Oregon", survey.arrival_port)
        self.assertIsNone(survey.creation_date)
        self.assertIsNone(survey.last_update)

        survey_parameters = cargo.related_survey_crate.survey_parameters
        self.assertEqual(9, len(survey_parameters))

        for survey_parameter in survey_parameters:
            self.assertTrue(isinstance(survey_parameter, CruiseSurveyParameter))
            self.assertIsNone(survey_parameter.id)
            self.assertIsNone(survey_parameter.survey_id)
            if survey_parameter.parameter_detail_name == "NAV1":
                self.assertEqual(57, survey_parameter.parameter_detail_id)
                self.assertEqual("GPS", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'NAV2':
                self.assertEqual(58, survey_parameter.parameter_detail_id)
                self.assertEqual("fake_nav2", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Horizontal_Datum':
                self.assertEqual(59, survey_parameter.parameter_detail_id)
                self.assertEqual("fake_hd", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Vertical_Datum':
                self.assertEqual(60, survey_parameter.parameter_detail_id)
                self.assertEqual("fake_vd", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Tide_Correction':
                self.assertEqual(61, survey_parameter.parameter_detail_id)
                self.assertEqual("fake_tc", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Sound_Velocity':
                self.assertEqual(62, survey_parameter.parameter_detail_id)
                self.assertEqual("fake_sv", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Comments':
                self.assertEqual(56, survey_parameter.parameter_detail_id)
                self.assertEqual("fake comment, I am", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Previous_State':
                self.assertEqual(63, survey_parameter.parameter_detail_id)
                self.assertEqual("No", survey_parameter.value)
            elif survey_parameter.parameter_detail_name == 'Proprietary':
                self.assertEqual(55, survey_parameter.parameter_detail_id)
                self.assertEqual("No", survey_parameter.value)
            else:
                self.assertTrue(False)  # must match a case

        survey_shape = cargo.related_survey_crate.survey_shape
        self.assertTrue(isinstance(survey_shape, CruiseShape))
        self.assertEqual("survey", survey_shape.shape_type)
        self.assertEqual("line", survey_shape.geom_type)
        self.assertEqual("LINESTRING (30 10, 10 30, 40 40)", survey_shape.shape)  # TODO
        self.assertIsNone(survey_shape.id)

        # dataset and dataset related tables
        dataset = cargo.dataset_crate.dataset
        self.assertTrue(isinstance(dataset, CruiseDataset))
        self.assertEqual("NEW2930", dataset.other_id)
        self.assertEqual("RR1808_EM122", dataset.dataset_name)
        self.assertEqual(DatasetTypeConsts.MB_RAW, dataset.dataset_type_name)
        self.assertEqual("EM122", dataset.instruments)
        self.assertEqual("Roger Revelle (RR)", dataset.platforms)
        self.assertEqual("04-SEP-19", dataset.archive_date)
        self.assertEqual("RR1808", dataset.surveys)
        self.assertEqual("Cascadia GPS-A", dataset.projects)
        self.assertEqual(DTLookup.get_id(DatasetTypeConsts.MB_RAW), dataset.dataset_type_id)
        self.assertIsNone(dataset.doi)
        self.assertIsNone(dataset.last_update)
        self.assertIsNone(dataset.id)

        self.assertEqual(1, len(cargo.dataset_crate.dataset_platforms))
        platform = cargo.dataset_crate.dataset_platforms[0]
        self.assertTrue(isinstance(platform, CruisePlatform))
        self.assertEqual("roger_revelle", platform.internal_name)
        self.assertEqual(PlatformTypeConsts.SHIP, platform.platform_type)
        self.assertIsNone(platform.docucomp_uuid)
        self.assertEqual("Roger Revelle", platform.long_name)
        self.assertEqual("RR", platform.designator)
        self.assertEqual("Roger Revelle", platform.platform_name)
        self.assertIsNone(platform.id)

        self.assertEqual(1, len(cargo.dataset_crate.dataset_instruments))
        instrument = cargo.dataset_crate.dataset_instruments[0]
        self.assertTrue(isinstance(instrument, CruiseInstrument))
        self.assertEqual("EM122", instrument.instrument_name)
        self.assertIsNone(instrument.docucomp_uuid)
        self.assertEqual("Kongsberg EM122", instrument.long_name)
        self.assertIsNone(instrument.id)

        self.assertEqual(1, len(cargo.dataset_crate.dataset_scientists))
        scientist = cargo.dataset_crate.dataset_scientists[0]
        self.assertTrue(isinstance(scientist, CruisePeopleAndSources))
        self.assertIsNone(scientist.id)
        self.assertEqual("C. David Chadwell", scientist.name)
        self.assertIsNone(scientist.position)
        self.assertEqual("Scripps Institution of Oceanography", scientist.organization)
        self.assertIsNone(scientist.street)
        self.assertIsNone(scientist.city)
        self.assertIsNone(scientist.state)
        self.assertIsNone(scientist.zipcode)
        self.assertIsNone(scientist.country)
        self.assertIsNone(scientist.phone)
        self.assertIsNone(scientist.email)
        self.assertIsNone(scientist.orcid)
        self.assertIsNone(scientist.docucomp_uuid)
        self.assertEqual("C. David", scientist.first)
        self.assertEqual("Chadwell", scientist.last)
        self.assertIsNone(scientist.prefix)
        self.assertIsNone(scientist.middle)
        self.assertIsNone(scientist.suffix)

        self.assertEqual(1, len(cargo.dataset_crate.dataset_sources))
        source = cargo.dataset_crate.dataset_sources[0]
        self.assertTrue(isinstance(source, CruisePeopleAndSources))
        self.assertIsNone(source.id)
        self.assertIsNone(source.name)
        self.assertIsNone(source.position)
        self.assertEqual("Rolling Deck to Repository (R2R)", source.organization)
        self.assertIsNone(source.street)
        self.assertIsNone(source.city)
        self.assertIsNone(source.state)
        self.assertIsNone(source.zipcode)
        self.assertIsNone(source.country)
        self.assertIsNone(source.phone)
        self.assertIsNone(source.email)
        self.assertIsNone(source.orcid)
        self.assertIsNone(source.docucomp_uuid)
        self.assertIsNone(source.first)
        self.assertIsNone(source.last)
        self.assertIsNone(source.prefix)
        self.assertIsNone(source.middle)
        self.assertIsNone(source.suffix)

        self.assertEqual(6, len(cargo.dataset_crate.dataset_parameters))
        dataset_parameters = cargo.dataset_crate.dataset_parameters
        for d_param in dataset_parameters:
            self.assertTrue(isinstance(d_param, CruiseDatasetParameter))
            self.assertIsNone(d_param.id)
            self.assertIsNone(d_param.dataset_id)

            if d_param.parameter_detail_name == 'Modify_Date_Data':
                self.assertEqual("05-MAY-20", d_param.value)  # MB.SURVEY.MODIFY_DATE_DATA
            elif d_param.parameter_detail_name == 'Modify_Date_Metadata':
                self.assertEqual("04-SEP-19", d_param.value)  # MB.SURVEY.MODIFY_DATE_METADATA
            elif d_param.parameter_detail_name == 'Extract_Metadata':
                self.assertEqual("yes", d_param.value)  # MB.SURVEY.EXTRACT_METADATA
            elif d_param.parameter_detail_name == 'Publish':
                self.assertEqual("yes", d_param.value)  # MB.SURVEY.PUBLISH
            elif d_param.parameter_detail_name == 'Previous_State':
                self.assertEqual("No", d_param.value)  # MB.SURVEY.PREVIOUS_STATE
            elif d_param.parameter_detail_name == 'Download_URL':
                self.assertEqual("https://www.ngdc.noaa.gov/ships/roger_revelle/RR1808_mb.html", d_param.value)  # MB.SURVEY_REFERENCE.DOWNLOAD_URL

            # current script only populates these if it is the only raw,processed,product dataset in the survey #
            # What it should be doing is deriving these values from the sums of like parameters in associated files. TODO: Validate that is doable with Data Managers
            # elif d_param.parameter_detail_name == 'Track_Length':
            #     self.assertEqual(0.8739, d_param.value)  # MB.SURVEY.TRACK_LENGTH
            # elif d_param.parameter_detail_name == 'Total_Time':
            #     self.assertEqual(0.0484, d_param.value)  # MB.SURVEY.TOTAL_TIME
            # elif d_param.parameter_detail_name == 'File_Count':
            #     self.assertEqual(142, d_param.value)  # MB.SURVEY.FILE_COUNT  # TODO: WHY SHOULDN'T THIS BE POPULATED FOR ALL DATASETS?
            # elif d_param.parameter_detail_name == 'Bathy_Beams':
            #     self.assertEqual(36583920, d_param.value)  # MB.SURVEY.BATHY_BEAMS
            # elif d_param.parameter_detail_name == 'Amp_Beams':
            #     self.assertEqual(85968, d_param.value)  # MB.SURVEY.AMP_BEAMS
            # elif d_param.parameter_detail_name == 'Sidescans':
            #     self.assertEqual(407552, d_param.value)  # MB.SURVEY.SIDESCANS
            # elif d_param.parameter_detail_name == 'Survey_Size':
            #     self.assertEqual(6797, d_param.value)  # d MB.SURVEY.SURVEY_SIZE  # TODO: WHY ISN'T THIS A SURVEY PARAMETER ?

            else:
                self.assertTrue(False)  # must match a case

        # project and project related tables
        project = cargo.related_project_crate.project
        self.assertTrue(isinstance(project, CruiseProject))
        self.assertEqual("Cascadia GPS-A", project.project_name)
        self.assertIsNone(project.id)

        project_parameters = cargo.related_project_crate.project_parameters
        self.assertFalse(project_parameters)

        # files and file related tables
        self.assertEqual(1, len(cargo.related_file_crates))
        file_crates = cargo.related_file_crates
        for crate in file_crates:
            file = crate.file
            self.assertTrue(isinstance(file, CruiseFile))
            self.assertEqual("0140_20180617_101452_revelle.all.mb58.gz", file.file_name)
            self.assertEqual(32143468, file.raw_size)
            self.assertEqual("Y", file.publish)
            self.assertEqual("04-SEP-19", file.collection_date)
            self.assertEqual("05-SEP-19", file.publish_date)
            self.assertEqual("05-SEP-19", file.archive_date)
            self.assertIsNone(file.temp_id)  # TODO verify this was created for old migration script only and is not used.
            self.assertEqual(15813031, file.gzip_size)
            self.assertIsNone(file.id)
            self.assertIsNone(file.dataset_id)
            self.assertEqual(1, file.version_id)
            self.assertEqual(1, file.type_id)
            self.assertEqual(65, file.format_id)
            self.assertIsNone(file.last_update)

            shape = crate.file_shape
            self.assertTrue(isinstance(shape, CruiseShape))
            self.assertEqual("file", shape.shape_type)
            self.assertEqual("line", shape.geom_type)
            self.assertEqual("LINESTRING (32 10, 30 10, 10 30)", shape.shape)
            self.assertIsNone(shape.id)

            self.assertEqual(2, len(crate.file_access_paths))
            access_paths = crate.file_access_paths
            for access_path in access_paths:
                self.assertTrue(isinstance(access_path, CruiseAccessPath))

                if access_path.path_type == "Disk":
                    self.assertEqual("ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122", access_path.path)  # MB.NGDCID_AND_FILE.DATA_FILE
                elif access_path.path_type == "Stornext":
                    self.assertEqual("/stornext/ngdc/archive/insitu_ocean/trackline/roger_revelle/rr1808/multibeam/data/version1/MB/em122", access_path.path)  # MB.NGDCID_AND_FILE.ARCHIVE_PATH
                else:
                    self.assertTrue(False)  # must be one of either stornext or disk path type
                self.assertIsNone(access_path.id)

            self.assertEqual(49, len(crate.file_parameters))
            file_parameters = crate.file_parameters
            for file_parameter in file_parameters:
                self.assertTrue(isinstance(file_parameter, CruiseFileParameter))
                self.assertIsNone(file_parameter.id)
                self.assertIsNone(file_parameter.file_id)
                if file_parameter.parameter_detail_name == 'MBIO_Format_ID':
                    self.assertEqual(58, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MBIO_FORMAT_ID
                elif file_parameter.parameter_detail_name == 'MB_RECORD_COUNT':
                    self.assertEqual(199, file_parameter.value)  # MB.MBINFO_FILE_TSQL.RECORD_COUNT
                elif file_parameter.parameter_detail_name == 'MB_BATHY_BEAMS':
                    self.assertEqual(85968, file_parameter.value)  # MB.MBINFO_FILE_TSQL.BATHY_BEAMS
                elif file_parameter.parameter_detail_name == 'MB_GOOD_BATH_TOTAL':
                    self.assertEqual(37828, file_parameter.value)  # MB.MBINFO_FILE_TSQL.BB_GOOD
                elif file_parameter.parameter_detail_name == 'MB_ZERO_BATH_TOTAL':
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.BB_ZERO
                elif file_parameter.parameter_detail_name == 'MB_FLAGGED_BATH_TOTAL':
                    self.assertEqual(48140, file_parameter.value)  # MB.MBINFO_FILE_TSQL.BB_FLAGGED
                elif file_parameter.parameter_detail_name == 'MB_AMP_BEAMS' or file_parameter.parameter_detail_name == "AMP_Beams":
                    self.assertEqual(85968, file_parameter.value)  # MB.MBINFO_FILE_TSQL.AMP_BEAMS
                elif file_parameter.parameter_detail_name == 'MB_GOOD_AMP_TOTAL' or file_parameter.parameter_detail_name == "AB_Good":
                    self.assertEqual(37828, file_parameter.value)  # MB.MBINFO_FILE_TSQL.AB_GOOD
                elif file_parameter.parameter_detail_name == 'MB_ZERO_AMP_TOTAL' or file_parameter.parameter_detail_name == "AB_Zero":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.AB_ZERO
                elif file_parameter.parameter_detail_name == 'MB_FLAGGED_AMP_TOTAL' or file_parameter.parameter_detail_name == "AB_Flagged":
                    self.assertEqual(48140, file_parameter.value)  # MB.MBINFO_FILE_TSQL.AB_FLAGGED
                elif file_parameter.parameter_detail_name == 'MB_SIDESCANS' or file_parameter.parameter_detail_name == "Sidescans":
                    self.assertEqual(407552, file_parameter.value)  # MB.MBINFO_FILE_TSQL.SIDESCANS
                elif file_parameter.parameter_detail_name == 'MB_GOOD_SIDESCANS_TOTAL' or file_parameter.parameter_detail_name == "SS_Good":
                    self.assertEqual(51130, file_parameter.value)  # MB.MBINFO_FILE_TSQL.SS_GOOD
                elif file_parameter.parameter_detail_name == 'MB_ZERO_SIDESCANS_TOTAL' or file_parameter.parameter_detail_name == "SS_Zero":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.SS_ZERO
                elif file_parameter.parameter_detail_name == 'MB_FLAGGED_SIDESCANS_TOTAL' or file_parameter.parameter_detail_name == "SS_Flagged":
                    self.assertEqual(356422, file_parameter.value)  # MB.MBINFO_FILE_TSQL.SS_FLAGGED
                elif file_parameter.parameter_detail_name == 'Total_Time' or file_parameter.parameter_detail_name == 'MB_TOTAL_TIME_HOURS':
                    self.assertEqual(0.0484, file_parameter.value)  # MB.MBINFO_FILE_TSQL.TOTAL_TIME
                elif file_parameter.parameter_detail_name == 'Track_Length' or file_parameter.parameter_detail_name == "MB_TOTAL_TRACK_LENGTH_KM":
                    self.assertEqual(0.8739, file_parameter.value)  # MB.MBINFO_FILE_TSQL.TRACK_LENGTH
                elif file_parameter.parameter_detail_name == 'AVG_Speed' or file_parameter.parameter_detail_name == "MB_AVG_SPEED_KM_HR":
                    self.assertEqual(18.0479, file_parameter.value)  # MB.MBINFO_FILE_TSQL.AVG_SPEED
                elif file_parameter.parameter_detail_name == 'Start_Time':
                    self.assertEqual("17-JUN-18", file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_TIME
                elif file_parameter.parameter_detail_name == 'Start_Lon':
                    self.assertEqual(-124.9368864, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_LON
                elif file_parameter.parameter_detail_name == 'Start_Lat':
                    self.assertEqual(43.9380677, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_LAT
                elif file_parameter.parameter_detail_name == 'Start_Depth':
                    self.assertEqual(526.6157, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_DEPTH
                elif file_parameter.parameter_detail_name == 'Start_Speed':
                    self.assertEqual(18.72, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_SPEED
                elif file_parameter.parameter_detail_name == 'Start_Heading':
                    self.assertEqual(29.79, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_HEADING
                elif file_parameter.parameter_detail_name == 'Start_Sonar_Depth':
                    self.assertEqual(6.1956, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_SONAR_DEPTH
                elif file_parameter.parameter_detail_name == 'Start_Sonar_Alt':
                    self.assertEqual(517.012, file_parameter.value)  # MB.MBINFO_FILE_TSQL.START_SONAR_ALT
                elif file_parameter.parameter_detail_name == 'End_Time':
                    self.assertEqual("17-JUN-18", file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_TIME
                elif file_parameter.parameter_detail_name == 'End_Lon':
                    self.assertEqual(-124.9315114, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_LON
                elif file_parameter.parameter_detail_name == 'End_Lat':
                    self.assertEqual(43.94489725, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_LAT
                elif file_parameter.parameter_detail_name == 'End_Depth':
                    self.assertEqual(452.7342, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_DEPTH
                elif file_parameter.parameter_detail_name == 'End_Speed':
                    self.assertEqual(18.72, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_SPEED
                elif file_parameter.parameter_detail_name == 'End_Heading':
                    self.assertEqual(31.93, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_HEADING
                elif file_parameter.parameter_detail_name == 'End_Sonar_Depth':
                    self.assertEqual(5.8218, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_SONAR_DEPTH
                elif file_parameter.parameter_detail_name == 'End_Sonar_Alt':
                    self.assertEqual(446.4576, file_parameter.value)  # MB.MBINFO_FILE_TSQL.END_SONAR_ALT
                elif file_parameter.parameter_detail_name == 'Min_Lon':
                    self.assertEqual(-124.941614557, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_LON
                elif file_parameter.parameter_detail_name == 'Max_Lon':
                    self.assertEqual(-124.929731436, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_LON
                elif file_parameter.parameter_detail_name == 'Min_Lat':
                    self.assertEqual(43.936409568, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_LAT
                elif file_parameter.parameter_detail_name == 'Max_Lat':
                    self.assertEqual(43.945754166, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_LAT
                elif file_parameter.parameter_detail_name == 'Min_Sonar_Depth' or file_parameter.parameter_detail_name == "MB_MIN_SONAR_DEPTH_M":
                    self.assertEqual(4.311, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_SONAR_DEPTH
                elif file_parameter.parameter_detail_name == 'Max_Sonar_Depth' or file_parameter.parameter_detail_name == "MB_MAX_SONAR_DEPTH_M":
                    self.assertEqual(7.2459, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_SONAR_DEPTH
                elif file_parameter.parameter_detail_name == 'Min_Sonar_Alt':
                    self.assertEqual(440.5044, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_SONAR_ALT
                elif file_parameter.parameter_detail_name == 'Max_Sonar_Alt':
                    self.assertEqual(1142.1681, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_SONAR_ALT
                elif file_parameter.parameter_detail_name == 'Min_Depth' or file_parameter.parameter_detail_name == "MB_MIN_DEPTH":
                    self.assertEqual(438.2145, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_DEPTH
                elif file_parameter.parameter_detail_name == 'Max_Depth' or file_parameter.parameter_detail_name == "MB_MAX_DEPTH":
                    self.assertEqual(1206.4799, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_DEPTH
                elif file_parameter.parameter_detail_name == 'Min_Amp' or file_parameter.parameter_detail_name == "MB_MIN_AMPLITUDE":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_AMP
                elif file_parameter.parameter_detail_name == 'Max_Amp' or file_parameter.parameter_detail_name == "MB_MAX_AMPLITUDE":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_AMP
                elif file_parameter.parameter_detail_name == 'Min_Sidescan' or file_parameter.parameter_detail_name == "MB_MIN_SIDESCAN":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MIN_SIDESCAN
                elif file_parameter.parameter_detail_name == 'Max_Sidescan' or file_parameter.parameter_detail_name == "MB_MAX_SIDESCAN":
                    self.assertEqual(0, file_parameter.value)  # MB.MBINFO_FILE_TSQL.MAX_SIDESCAN
                elif file_parameter.parameter_detail_name == 'Object_ID':
                    self.assertEqual(1704625, file_parameter.value)  # MB.MBINFO_FILE_TSQL.OBJECTID
                else:
                    self.assertTrue(False)  # parameter must match one of these cases

    def _create_standard_test_mb_survey_crate(self):
        mb_survey = self._get_standard_test_mb_survey()
        mb_survey_reference = self._get_standard_survey_reference()

        return MbSurveyCrate(survey=mb_survey, survey_reference=mb_survey_reference, shape="LINESTRING (30 10, 10 30, 40 40)")

    def _create_standard_test_mb_file_crates(self):
        mbfile = self._get_standard_test_file()
        mbinfo = self._get_standard_test_mbinfo()
        mbfile.label = FileLabels.STANDARD
        file_crate1 = MbFileCrate(mb_file=mbfile, mb_info=mbinfo, shape="LINESTRING (32 10, 30 10, 10 30)")
        file_crates = FileDecoder.decode([file_crate1])

        return file_crates

    @staticmethod
    def _get_standard_test_mb_survey():
        return MbSurvey(
            ngdc_id="NEW2930",
            chief_scientist="Chadwell, C. David",
            departure_port="Newport, Oregon",
            arrival_port="Newport, Oregon",
            start_time=datetime.datetime.strptime("13-JUN-18", "%d-%b-%y"),
            end_time=datetime.datetime.strptime("17-JUN-18", "%d-%b-%y"),
            survey_name="RR1808",
            ship_name="Roger Revelle",
            source="Rolling Deck to Repository (R2R)",
            nav1="GPS",
            nav2="fake_nav2",
            instrument="Kongsberg EM122",
            horizontal_datum="fake_hd",
            vertical_datum="fake_vd",
            tide_correction="fake_tc",
            sound_velocity="fake_sv",
            ship_owner=None,
            project_name="Cascadia GPS-A",
            contact_id=None,
            chief_sci_organization="Scripps Institution of Oceanography",
            publish="yes",
            comments="fake comment, I am",
            proprietary="No",
            entered_date="04-SEP-19",
            previous_state="No",
            file_count=142,
            track_length=965.8628,
            total_time=68.5061,
            bathy_beams=36583920,
            amp_beams=36583920,
            sidescans=173434880,
            survey_size=6797,
            modify_date_data="05-MAY-20",
            modify_date_metadata="04-SEP-19",
            extract_metadata="yes"
        )

    @staticmethod
    def _get_standard_survey_reference():
        return SurveyReference(
            ngdc_id="NEW2930",
            doi=None,
            abstract=None,
            purpose=None,
            project_url=None,
            create_date="05-SEP-19",
            created_by="initial load",
            last_update_date=None,
            last_updated_by=None,
            download_url="https://www.ngdc.noaa.gov/ships/roger_revelle/RR1808_mb.html"
        )

    @staticmethod
    def _get_standard_test_file():
        file1 = MbFile(
            ngdc_id="NEW2930",
            data_file="ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0140_20180617_101452_revelle.all.mb58.gz",
            format_id=58,
            entry_date="04-SEP-19",
            process_date="05-SEP-19",
            status="Processed by jdbload-mb_track with /opt/gis_contrib/bin/mbinfo -G -F 58 -I/mgg/MB/ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0140_20180617_101452_revelle.all.mb58",
            version=1,
            mostcurrent=1,
            version_id=0,
            process_notes="min_amp < min amp: -77.8 truncated to 0.0, max_amp < min amp: -20.3 truncated to 0.0, min_sidescan < min sidescan value: -84.55 truncated to 0.0, max_sidescan < min sidescan value: -20.3 truncated to 0.0",
            filesize=32143468,
            filesize_gzip=15813031,
            filenotfound=None,
            publish="yes",
            previous_state="No",
            archive_path="/stornext/ngdc/archive/insitu_ocean/trackline/roger_revelle/rr1808/multibeam/data/version1/MB/em122/0140_20180617_101452_revelle.all.mb58.gz"
        )
        file1.parsed_file = ParsedFilePath(file1.data_file)

        return file1

        # file2 = MbFile(
        #     ngdc_id="NEW2930",
        #     data_file="ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0150_20180617_151453_revelle.all.mb58.gz",
        #     format_id=58,
        #     entry_date="04-SEP-19",
        #     process_date="05-SEP-19",
        #     status="Processed by jdbload-mb_track with /opt/gis_contrib/bin/mbinfo -G -F 58 -I/mgg/MB/ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0150_20180617_151453_revelle.all.mb58",
        #     version=1,
        #     mostcurrent=1,
        #     version_id=0,
        #     process_notes="min_amp < min amp: -75.1 truncated to 0.0, max_amp < min amp: -0.9 truncated to 0.0, min_sidescan < min sidescan value: -97.9 truncated to 0.0, max_sidescan < min sidescan value: -10.2 truncated to 0.0",
        #     filesize=23576814,
        #     filesize_gzip=13715710,
        #     filenotfound=None,
        #     publish="yes",
        #     previous_state="No",
        #     archive_path="/stornext/ngdc/archive/insitu_ocean/trackline/roger_revelle/rr1808/multibeam/data/version1/MB/em122/0150_20180617_151453_revelle.all.mb58.gz"
        # )

        # return file1, file2

    @staticmethod
    def _get_standard_test_mbinfo():

        mbinfo1 = MbInfo(
            data_file="ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0140_20180617_101452_revelle.all.mb58.gz",
            ngdc_id="NEW2930",
            mbio_format_id=58,
            record_count=199,
            bathy_beams=85968,
            bb_good=37828,
            bb_zero=0,
            bb_flagged=48140,
            amp_beams=85968,
            ab_good=37828,
            ab_zero=0,
            ab_flagged=48140,
            sidescans=407552,
            ss_good=51130,
            ss_zero=0,
            ss_flagged=356422,
            total_time=0.0484,
            track_length=0.8739,
            avg_speed=18.0479,
            start_time="17-JUN-18",
            start_lon=-124.9368864,
            start_lat=43.9380677,
            start_depth=526.6157,
            start_speed=18.72,
            start_heading=29.79,
            start_sonar_depth=6.1956,
            start_sonar_alt=517.012,
            end_time="17-JUN-18",
            end_lon=-124.9315114,
            end_lat=43.94489725,
            end_depth=452.7342,
            end_speed=18.72,
            end_heading=31.93,
            end_sonar_depth=5.8218,
            end_sonar_alt=446.4576,
            min_lon=-124.941614557,
            max_lon=-124.929731436,
            min_lat=43.936409568,
            max_lat=43.945754166,
            min_sonar_depth=4.311,
            max_sonar_depth=7.2459,
            min_sonar_alt=440.5044,
            max_sonar_alt=1142.1681,
            min_depth=438.2145,
            max_depth=1206.4799,
            min_amp=0,
            max_amp=0,
            min_sidescan=0,
            max_sidescan=0,
            objectid=1704625,
            shape=None,  # MDSYS.SDO_GEOMETRY(2002, 8307, NULL, MDSYS.SDO_ELEM_INFO_ARRAY(1, 2, 1), MDSYS.SDO_ORDINATE_ARRAY(-124.9368864, 43.9380677, -124.9315114, 43.94489725))
            publish="yes",
            previous_state="No",
            shape_gen=None  # MDSYS.SDO_GEOMETRY(2002, 8307, NULL, MDSYS.SDO_ELEM_INFO_ARRAY(1, 2, 1), MDSYS.SDO_ORDINATE_ARRAY(-124.9368864, 43.9380677, -124.9315114, 43.94489725))
        )

        return mbinfo1

        # mbinfo2 = MbInfo(
        #     data_file="ocean/ships/roger_revelle/RR1808/multibeam/data/version1/MB/em122/0150_20180617_151453_revelle.all.mb58.gz",
        #     ngdc_id="NEW2930",
        #     mbio_format_id=58,
        #     record_count=619,
        #     bathy_beams=267408,
        #     bb_good=218558,
        #     bb_zero=0,
        #     bb_flagged=48850,
        #     amp_beams=267408,
        #     ab_good=218558,
        #     ab_zero=0,
        #     ab_flagged=48850,
        #     sidescans=1267712,
        #     ss_good=476874,
        #     ss_zero=0,
        #     ss_flagged=790838,
        #     total_time=0.0458,
        #     track_length=0.8038,
        #     avg_speed=17.5349,
        #     start_time="17-JUN-18",
        #     start_lon=-124.3676899,
        #     start_lat=44.3984174,
        #     start_depth=231.9126,
        #     start_speed=17.424,
        #     start_heading=38.5,
        #     start_sonar_depth=5.2363,
        #     start_sonar_alt=226.8021,
        #     end_time="17-JUN-18",
        #     end_lon=-124.3609625,
        #     end_lat=44.4037969,
        #     end_depth=147.8297,
        #     end_speed=17.424,
        #     end_heading=41.41,
        #     end_sonar_depth=5.8082,
        #     end_sonar_alt=142.0824,
        #     min_lon=-124.368744437,
        #     max_lon=-124.359581432,
        #     min_lat=44.397857001,
        #     max_lat=44.404673958,
        #     min_sonar_depth=4.5649,
        #     max_sonar_depth=6.9716,
        #     min_sonar_alt=141.3245,
        #     max_sonar_alt=226.8021,
        #     min_depth=101.3383,
        #     max_depth=242.115,
        #     min_amp=0,
        #     max_amp=0,
        #     min_sidescan=0,
        #     max_sidescan=0,
        #     objectid=1704626,
        #     shape=None,  # MDSYS.SDO_GEOMETRY(2002, 8307, NULL, MDSYS.SDO_ELEM_INFO_ARRAY(1, 2, 1), MDSYS.SDO_ORDINATE_ARRAY(-124.3676899, 44.3984174, -124.3609625, 44.4037969))
        #     publish="yes",
        #     previous_state="No",
        #     shape_gen=None  # MDSYS.SDO_GEOMETRY(2002, 8307, NULL, MDSYS.SDO_ELEM_INFO_ARRAY(1, 2, 1), MDSYS.SDO_ORDINATE_ARRAY(-124.3676899, 44.3984174, -124.3609625, 44.4037969))
        # )
        #
        # return mbinfo1, mbinfo2
