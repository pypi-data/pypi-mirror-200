"""Сlass inherits from base class of TrainaleModel with a specific method for fine-tuning the model."""
from abc import ABC, abstractmethod

from ML_management.models.TrainableModel import TrainableModel

# TODO does Retrainable model have to be Trainable?


class RetrainableModel(TrainableModel, ABC):
    """Implementation of retrainble model."""

    def __init__(self):
        super().__init__()
        self._finetune_data_path = None

    @property
    def finetune_data_path(self):
        """Get data path property."""
        # do i need to raise if self._data_path is uninitialized?
        return self._finetune_data_path

    @finetune_data_path.setter
    def finetune_data_path(self, path: str):
        """Set data path property."""
        self._finetune_data_path = path

    @abstractmethod
    def finetune_function(
        self,
    ):
        """Define finetune_mode."""
        raise NotImplementedError
