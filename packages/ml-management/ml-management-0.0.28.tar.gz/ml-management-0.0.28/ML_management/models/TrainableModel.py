"""Сlass inherits from base class of Model with a specific method for training the model."""
from abc import ABC, abstractmethod

from ML_management.models.model_pattern import Model


class TrainableModel(Model, ABC):
    """Implementation of trainable model."""

    def __init__(self):
        super().__init__()
        self._train_data_path = None

    @property
    def train_data_path(self):
        """Get data path property."""
        # do i need to raise if self._data_path is uninitialized?
        return self._train_data_path

    @train_data_path.setter
    def train_data_path(self, path: str):
        """Set data path property."""
        self._train_data_path = path

    @abstractmethod
    def train_function(
        self,
    ):
        """Define train_function."""
        raise NotImplementedError
