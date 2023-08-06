from typing import Callable

from src.mb_cruise_migration.utility.dataset import get_dataset_instrument, get_designator, build_dataset_name, build_platform_name

from src.mb_cruise_migration.models.intermediary.prefab import Prefab
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbSurveyCrate, MbFileCrate
from src.mb_cruise_migration.framework.resolvers.dataset_type_resolver import DatasetTypeConsts
from src.mb_cruise_migration.framework.consts.file_label_consts import FileLabels
from src.mb_cruise_migration.framework.consts.platform_type_consts import PlatformTypeResolver
from src.mb_cruise_migration.framework.consts.error_consts import ErrorConsts


class PrefabFactory(object):
    @classmethod
    def construct_prefab(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:
        fabricator = cls.__get_fabricator(file_context.mb_file.label)
        return fabricator(file_context, survey_context)

    @classmethod
    def __get_fabricator(cls, label: str) -> Callable:
        if label == FileLabels.STANDARD:
            return cls.__new_standard
        if label == FileLabels.SURVEY_METADATA:
            return cls.__new_survey_metadata
        if label == FileLabels.EXTRANEOUS:
            return cls.__new_extraneous
        if label == FileLabels.LEG:
            return cls.__new_with_leg
        if label == FileLabels.ZONE:
            return cls.__new_with_zone
        if label == FileLabels.REGION:
            return cls.__new_with_region

        raise RuntimeError(ErrorConsts.NO_PREFAB_FABRICATOR)

    @classmethod
    def __new_survey_metadata(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:

        is_nonpublic = False
        file_type = file_context.file_type
        dataset_type = DatasetTypeConsts.METADATA
        dataset_name = build_dataset_name(dataset_type, survey_context.mb_survey.survey_name, None, None)

        return Prefab(
            other_id=file_context.mb_file.ngdc_id,
            dataset_name=dataset_name,
            dataset_type_name=dataset_type,
            instrument=None,
            platform=None,
            archive_date=survey_context.mb_survey.entered_date,
            survey=survey_context.mb_survey.survey_name,
            project=survey_context.mb_survey.project_name,
            path_platform_type=None,
            path_platform_name=None,
            level=None,
            platform_designator=None,
            is_nonpublic=is_nonpublic,
            files_type=file_type
        )

    @classmethod
    def __new_extraneous(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:
        raise NotImplementedError("Migration of files with extraneous path parts not supported at this time")

    @classmethod
    def __new_with_leg(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:
        raise NotImplementedError("Migration of files in surveys using legs not supported at this time")

    @classmethod
    def __new_with_zone(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:
        raise NotImplementedError("Migration of files in surveys using zones not supported at this time")

    @classmethod
    def __new_with_region(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:
        raise NotImplementedError("Migration of files in surveys using regions not supported at this time")

    @classmethod
    def __new_standard(cls, file_context: MbFileCrate, survey_context: MbSurveyCrate) -> Prefab:

        dataset_type = file_context.dataset_type
        path_platform_name = file_context.platform_name
        path_platform_type = file_context.platform_type

        dataset_instrument = get_dataset_instrument(dataset_type, file_context, survey_context.mb_survey.instrument)
        dataset_name = build_dataset_name(dataset_type, survey_context.mb_survey.survey_name, dataset_instrument, survey_context.provider)

        platform_designator = get_designator(path_platform_name, survey_context.mb_survey.ship_name)
        platform_name = build_platform_name(survey_context.mb_survey.ship_name, platform_designator)
        platform_type = PlatformTypeResolver.resolve_platform_from_path_derived_platform(path_platform_type)

        return Prefab(
            other_id=file_context.mb_file.ngdc_id,
            dataset_name=dataset_name,
            dataset_type_name=dataset_type,
            instrument=dataset_instrument,
            platform=platform_name,
            archive_date=survey_context.mb_survey.entered_date,
            survey=survey_context.mb_survey.survey_name,
            project=survey_context.mb_survey.project_name,
            path_platform_type=platform_type,
            path_platform_name=path_platform_name,
            level=file_context.level,
            platform_designator=platform_designator,
            is_nonpublic=file_context.non_public,
            files_type=file_context.file_type,
        )
