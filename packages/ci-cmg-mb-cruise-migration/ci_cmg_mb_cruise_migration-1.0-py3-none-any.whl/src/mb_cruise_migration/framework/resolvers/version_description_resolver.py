from typing import Optional

from src.mb_cruise_migration.framework.consts.version_consts import VersionConsts
from src.mb_cruise_migration.framework.consts.version_description_consts import VersionDescriptionConsts
from src.mb_cruise_migration.framework.resolvers.file_type_resolver import FileTypeConsts
from src.mb_cruise_migration.models.cruise.cruise_version_descriptions import CruiseVersionDescription


class VDLookup(object):
    LOOKUP_description = {}
    LOOKUP_version_level = {}
    LOOKUP_version_number = {}

    @staticmethod
    def set_lookups(descriptions: [CruiseVersionDescription]):
        for description in descriptions:
            VDLookup.LOOKUP_description.update({description.description: description})
            VDLookup.LOOKUP_description.update({description.version_level: description})
            VDLookup.LOOKUP_description.update({description.version_number: description})

    @classmethod
    def get_id(cls, file_type, version: Optional[str]) -> Optional[int]:
        if file_type == FileTypeConsts.MB_RAW:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.RAW)
        if file_type == FileTypeConsts.MB_PROCESSED:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.PROCESSED)
        if file_type == FileTypeConsts.MB_PRODUCT:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.PRODUCT)
        if file_type == FileTypeConsts.METADATA:
            if version:
                return cls.__get_id_from_version(version)
            return VDLookup.get_id_from_description(VersionDescriptionConsts.METADATA)
        if file_type == FileTypeConsts.DOCUMENT:
            if version:
                return cls.__get_id_from_version(version)
            return VDLookup.get_id_from_description(VersionDescriptionConsts.DOCUMENT)
        if file_type == FileTypeConsts.ANCILLARY:
            if version:
                return cls.__get_id_from_version(version)
            return VDLookup.get_id_from_description(VersionDescriptionConsts.ANCILLARY)

    @staticmethod
    def __get_id_from_version(version):
        if version == VersionConsts.VERSION1:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.RAW)
        if version == VersionConsts.VERSION2:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.PROCESSED)
        if version == VersionConsts.VERSION3:
            return VDLookup.get_id_from_description(VersionDescriptionConsts.PRODUCT)

    @staticmethod
    def get_id_from_description(description: str) -> Optional[int]:
        try:
            version_description = VDLookup.LOOKUP_description[description]
            return version_description.id
        except KeyError:
            return None

    @staticmethod
    def get_version_number_from_description(description: str) -> Optional[int]:
        try:
            version_description = VDLookup.LOOKUP_description[description]
            return version_description.version_number
        except KeyError:
            return None

    @staticmethod
    def validate():
        for key, value in vars(VersionDescriptionConsts).items():
            if key == '__module__' or key == '__dict__' or key == '__weakref__' or key == '__doc__':
                continue
            if VDLookup.get_id_from_description(value) is None:
                raise ValueError(f"Version description value {value} for constant {key} does not exist in cruise db.")
