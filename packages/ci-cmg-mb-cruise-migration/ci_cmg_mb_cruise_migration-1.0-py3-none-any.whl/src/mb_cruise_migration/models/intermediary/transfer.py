from __future__ import annotations

from src.mb_cruise_migration.models.intermediary.cruise_cargo import CruiseCargo, CruiseDatasetCrate
from src.mb_cruise_migration.models.intermediary.prefab import Prefab
from src.mb_cruise_migration.models.intermediary.mb_cargo import MbFileCrate, MbSurveyCrate
from src.mb_cruise_migration.processors.prefab_factory import PrefabFactory
from src.mb_cruise_migration.processors.schema_mapper import SchemaMapper


class Transfer(object):
    """
    transfers metadata from mb schema relational objects to cruise schema relational objects
    """

    def __init__(self, mb_survey_crate: MbSurveyCrate, prefab: Prefab, mb_file_crates: [MbFileCrate]):
        self.mb_survey_crate: MbSurveyCrate = mb_survey_crate
        self.prefab = prefab
        self.mb_file_crates = mb_file_crates

    def load_cruise_cargo(self) -> CruiseCargo:
        """
        populates known and derived values into cruise schema objects and
        packages them into a cruise cargo container for db insertion
        """
        mb_survey = self.mb_survey_crate.mb_survey
        survey_reference = self.mb_survey_crate.mb_survey_references
        prefab = self.prefab
        files = self.mb_file_crates

        dataset = SchemaMapper.load_dataset(prefab)
        dataset_parameters = SchemaMapper.load_dataset_parameters(mb_survey, survey_reference)
        platforms = SchemaMapper.load_platforms(mb_survey, prefab) if prefab.platform else None
        scientists = SchemaMapper.load_scientists(mb_survey)
        sources = SchemaMapper.load_sources(mb_survey)
        instruments = SchemaMapper.load_instruments(mb_survey, prefab)

        dataset_crate = CruiseDatasetCrate(
            dataset=dataset,
            dataset_parameters=dataset_parameters,
            dataset_platforms=platforms,
            dataset_scientists=scientists,
            dataset_sources=sources,
            dataset_instruments=instruments
        )
        survey_crate = SchemaMapper.load_survey_crate(self.mb_survey_crate)
        project_crate = SchemaMapper.load_project_crate(mb_survey)
        file_crates = SchemaMapper.load_file_crates(files, prefab)

        return CruiseCargo(
            dataset_crate=dataset_crate,
            survey_crates=survey_crate,
            project_crates=project_crate,
            file_crates=file_crates
        )

    @staticmethod
    def build(survey_crate: MbSurveyCrate, file_crate: MbFileCrate):
        prefab = PrefabFactory.construct_prefab(file_crate, survey_crate)
        return Transfer(survey_crate, prefab, [file_crate])
