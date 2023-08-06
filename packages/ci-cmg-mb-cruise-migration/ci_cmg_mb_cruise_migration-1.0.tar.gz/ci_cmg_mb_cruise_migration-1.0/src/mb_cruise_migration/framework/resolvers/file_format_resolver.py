from typing import Optional

from src.mb_cruise_migration.framework.consts.file_format_consts import FileFormatConsts
from src.mb_cruise_migration.models.cruise.cruise_file_formats import CruiseFileFormat
from src.mb_cruise_migration.models.mb.mb_mbinfo_formats import MbFileFormat


class FFLookup(object):

    LOOKUP_id = {}
    LOOKUP_name = {}

    @staticmethod
    def set_id_lookup(file_formats: [CruiseFileFormat]):
        for file_format in file_formats:
            FFLookup.LOOKUP_id.update({file_format.format_name: file_format.id})

    @staticmethod
    def set_name_lookup(file_formats: [MbFileFormat]):
        for file_format in file_formats:
            FFLookup.LOOKUP_name.update({file_format.id: file_format.format_name})

    @staticmethod
    def get_id(mb_format_name) -> Optional[int]:
        try:
            return FFLookup.LOOKUP_id[mb_format_name]
        except KeyError:
            return None

    @staticmethod
    def get_name(mb_format_id) -> Optional[str]:
        try:
            return FFLookup.LOOKUP_name[mb_format_id]
        except KeyError:
            return None

    @staticmethod
    def validate():
        expected_mb_format_names = []
        found_mb_format_names = FFLookup.LOOKUP_name.values()
        for key, value in vars(FileFormatConsts).items():
            if key == '__module__' or key == '__dict__' or key == '__weakref__' or key == '__doc__':
                continue
            if FFLookup.get_id(value) is None:
                # raise ValueError(f"File type value {value} for constant {key} does not exist in CRUISE db.")
                print(f"File type value {value} for constant {key} does not exist in CRUISE db.")
            expected_mb_format_names.append(value)

        for found in found_mb_format_names:
            if found not in expected_mb_format_names:
                # raise ValueError(f"File type value {found} for MB db not found in constants for file formats as expected")
                print(f"File type value {found} for MB db not found in constants for file formats as expected")
