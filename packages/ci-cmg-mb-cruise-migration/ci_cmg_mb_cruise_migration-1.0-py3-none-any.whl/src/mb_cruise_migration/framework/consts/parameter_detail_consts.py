from typing import Optional

from src.mb_cruise_migration.models.cruise.cruise_parameter_details import CruiseParameterDetail
from src.mb_cruise_migration.services.cruise_service import ParameterDetailService


class PDLookup(object):
    LOOKUP = {}

    @staticmethod
    def set_lookup(parameter_details: [CruiseParameterDetail]):
        for parameter_detail in parameter_details:
            PDLookup.LOOKUP.update({parameter_detail.parameter: parameter_detail.parameter_id})

    @staticmethod
    def get_id(parameter: str) -> Optional[int]:
        try:
            return PDLookup.LOOKUP[parameter]
        except KeyError:
            return None

    @staticmethod
    def validate(parameter_detail_service):
        for key, value in vars(ParameterDetailConsts).items():
            if key == '__module__' or key == '__dict__' or key == '__weakref__' or key == '__doc__':
                continue
            if PDLookup.get_id(value) is None:
                parameter_detail_service.save_new_parameter_detail(CruiseParameterDetail(parameter=value, parameter_type=None, description=None))
                # TODO Log this instead:
                # raise ValueError(f"File type value {value} for constant {key} does not exist in cruise db.")


class ParameterDetailConsts(object):
    FILE_FORMAT_TYPE = "FILE_FORMAT_TYPE"
    FILE_FORMAT_PROTOCOL = "FILE_FORMAT_PROTOCOL"
    FILE_FORMAT_ATTRIBUTES = "FILE_FORMAT_ATTRIBUTES"
    MB_SYSTEM_ID = "MB_SYSTEM_ID"
    MB_FILE_FORMAT_ID = "MB_FILE_FORMAT_ID"
    MD5_CHECKSUM = "MD5_CHECKSUM"
    SHA256_CHECKSUM = "SHA256_CHECKSUM"
    MB_OBJECT_COUNT = "MB_OBJECT_COUNT"
    MB_TOTAL_TIME_HOURS = "MB_TOTAL_TIME_HOURS"
    MB_TOTAL_TRACK_LENGTH_KM = "MB_TOTAL_TRACK_LENGTH_KM"  # a.k.a 'Track_Length'
    MB_AVG_SPEED_KM_HR = "MB_AVG_SPEED_KM_HR"  # a.k.a 'AVG_Speed'
    MB_MIN_SONAR_DEPTH_M = "MB_MIN_SONAR_DEPTH_M"  # a.k.a "Min_Sonar_Depth"
    MB_MAX_SONAR_DEPTH_M = "MB_MAX_SONAR_DEPTH_M"  # a.k.a "Max_Sonar_Depth"
    MB_MIN_ALTITUDE = "MB_MIN_ALTITUDE"
    MB_MAX_ALTITUDE = "MB_MAX_ALTITUDE"
    MB_MIN_DEPTH = "MB_MIN_DEPTH"  # a.k.a 'Min_Depth'
    MB_MAX_DEPTH = "MB_MAX_DEPTH"  # a.k.a 'Max_Depth'
    MB_MIN_AMPLITUDE = "MB_MIN_AMPLITUDE"  # a.k.a 'Min_Amp'
    MB_MAX_AMPLITUDE = "MB_MAX_AMPLITUDE"  # a.k.a 'Max_Amp'
    MB_MIN_SIDESCAN = "MB_MIN_SIDESCAN"  # a.k.a 'Min_Sidescan'
    MB_MAX_SIDESCAN = "MB_MAX_SIDESCAN"  # a.k.a 'Max_Sidescan'
    MB_FILE_COUNT = "MB_FILE_COUNT"
    MB_RECORD_COUNT = "MB_RECORD_COUNT"
    MB_BATHY_BEAMS = "MB_BATHY_BEAMS"
    MB_GOOD_BATH_TOTAL = "MB_GOOD_BATH_TOTAL"
    MB_GOOD_BATH_PERCENT = "MB_GOOD_BATH_PERCENT"
    MB_ZERO_BATH_TOTAL = "MB_ZERO_BATH_TOTAL"
    MB_ZERO_BATH_PERCENT = "MB_ZERO_BATH_PERCENT"
    MB_FLAGGED_BATH_TOTAL = "MB_FLAGGED_BATH_TOTAL"
    MB_FLAGGED_BATH_PERCENT = "MB_FLAGGED_BATH_PERCENT"
    MB_AMP_BEAMS = "MB_AMP_BEAMS"     # a.k.a. 'AMP_Beams'
    MB_GOOD_AMP_TOTAL = "MB_GOOD_AMP_TOTAL"   # a.k.a. 'AB_Good'
    MB_GOOD_AMP_PERCENT = "MB_GOOD_AMP_PERCENT"
    MB_ZERO_AMP_TOTAL = "MB_ZERO_AMP_TOTAL"  # a.k.a 'AB_Zero'
    MB_ZERO_AMP_PERCENT = "MB_ZERO_AMP_PERCENT"
    MB_FLAGGED_AMP_TOTAL = "MB_FLAGGED_AMP_TOTAL"  # a.k.a. 'AB_Flagged'
    MB_FLAGGED_AMP_PERCENT = "MB_FLAGGED_AMP_PERCENT"
    MB_SIDESCANS = "MB_SIDESCANS"  # a.k.a.'Sidescans'
    MB_GOOD_SIDESCANS_TOTAL = "MB_GOOD_SIDESCANS_TOTAL"  # a.k.a 'SS_Good'
    MB_GOOD_SIDESCANS_PERCENT = "MB_GOOD_SIDESCANS_PERCENT"
    MB_ZERO_SIDESCANS_TOTAL = "MB_ZERO_SIDESCANS_TOTAL"  # a.k.a 'SS_Zero'
    MB_ZERO_SIDESCANS_PERCENT = "MB_ZERO_SIDESCANS_PERCENT"
    MB_FLAGGED_SIDESCANS_TOTAL = "MB_FLAGGED_SIDESCANS_TOTAL"  # a.k.a 'SS_Flagged'
    MB_FLAGGED_SIDESCANS_PERCENT = "MB_FLAGGED_SIDESCANS_PERCENT"
    MB_BBOX_NORTH = "MB_BBOX_NORTH"
    MB_BBOX_SOUTH = "MB_BBOX_SOUTH"
    MB_BBOX_EAST = "MB_BBOX_EAST"
    MB_BBOX_WEST = "MB_BBOX_WEST"
    DIRECTORY_STRUCTURE_TYPE = "DIRECTORY_STRUCTURE_TYPE"
    MB_NGDC_ID = "MB_NGDC_ID"
    MB_DATASET_DIR = "MB_DATASET_DIR"
    DATASET_DIRECTORY = "DATASET_DIRECTORY"
    MB_AREA_SQ_KM = "MB_AREA_SQ_KM"
    PUBLISH = "Publish"
    PROPRIETARY = "Proprietary"
    COMMENTS = "Comments"
    NAV1 = "NAV1"
    NAV2 = "NAV2"
    HORIZONTAL_DATUM = "Horizontal_Datum"
    VERTICAL_DATUM = "Vertical_Datum"
    TIDE_CORRECTION = "Tide_Correction"
    SOUND_VELOCITY = "Sound_Velocity"
    PREVIOUS_STATE = "Previous_State"
    MODIFY_DATE_DATA = "Modify_Date_Data"
    MODIFY_DATE_METADATA = "Modify_Date_Metadata"
    EXTRACT_METADATA = "Extract_Metadata"
    DOWNLOAD_URL = "Download_URL"
    MBIO_FORMAT_ID = "MBIO_Format_ID"

    MB_START_TIME = "Start_Time"
    MB_START_LONGITUDE = "Start_Lon"
    MB_START_LATITUDE = "Start_Lat"
    MB_START_DEPTH = "Start_Depth"
    MB_START_SPEED = "Start_Speed"
    MB_START_HEADING = "Start_Heading"
    MB_START_SONAR_DEPTH = "Start_Sonar_Depth"
    MB_START_SONAR_ALTITUDE = "Start_Sonar_Alt"
    MB_END_TIME = "End_Time"
    MB_END_LONGITUDE = "End_Lon"
    MB_END_LATITUDE = "End_Lat"
    MB_END_DEPTH = "End_Depth"
    MB_END_SPEED = "End_Speed"
    MB_END_HEADING = "End_Heading"
    MB_END_SONAR_DEPTH = "End_Sonar_Depth"
    MB_END_SONAR_ALTITUDE = "End_Sonar_Alt"
    MB_MIN_LONGITUDE = "Min_Lon"
    MB_MAX_LONGITUDE = "Max_Lon"
    MB_MIN_LATITUDE = "Min_Lat"
    MB_MAX_LATITUDE = "Max_Lat"
    MB_MIN_SONAR_ALTITUDE = "Min_Sonar_Alt"
    MB_MAX_SONAR_ALTITUDE = "Max_Sonar_Alt"
    MB_OBJECT_ID = "Object_ID"
