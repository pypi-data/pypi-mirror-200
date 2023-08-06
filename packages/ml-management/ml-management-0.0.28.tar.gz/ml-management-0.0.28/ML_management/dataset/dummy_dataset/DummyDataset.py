"""Dummy dataset inherited from the base abstract class."""
from ML_management.dataset.datamodel import DatasetFlavour
from ML_management.dataset.Dataset import Dataset


class DummyDataset(Dataset):
    """Implementation of DummyLoader Dataset."""

    def get_json_schema(self):
        """Return empty json schema."""
        schema = {}
        return schema

    def set_data(self, *args, **kwargs):
        """Return empty string."""
        return ""

    def get_data_flavour():
        """Return flavour."""
        return DatasetFlavour.DummyDataset
