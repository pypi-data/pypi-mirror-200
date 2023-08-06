from typing import Optional

from src.mb_cruise_migration.framework.consts.dataset_type_consts import DatasetTypeConsts
from src.mb_cruise_migration.models.cruise.cruise_dataset_types import CruiseDatasetType


class DTLookup(object):
    LOOKUP = {}

    @staticmethod
    def set_lookup(dataset_types: [CruiseDatasetType]):
        for dataset_type in dataset_types:
            DTLookup.LOOKUP.update({dataset_type.type_name: dataset_type.id})

    @staticmethod
    def get_id(dataset_type: str) -> Optional[int]:
        try:
            return DTLookup.LOOKUP[dataset_type]
        except KeyError:
            return None

    @staticmethod
    def validate():
        for key, value in vars(DatasetTypeConsts).items():
            if key == '__module__' or key == '__dict__' or key == '__weakref__' or key == '__doc__' or key == 'get_dataset_type' or key == 'dataset_has_associated_instrument':
                continue
            if DTLookup.get_id(value) is None:
                raise ValueError(f"Dataset type value {value} for constant {key} does not exist in cruise db.")
