"""Define Abstract class for Model with neccessary methods and methods to implement."""
from abc import ABC, abstractmethod

from ML_management import mlmanagement
from ML_management.models.action_type import ActionType

import mlflow


class Model(mlflow.pyfunc.PythonModel, ABC):
    """Abstract class for model that Job will use."""

    def __init__(self):
        """Get model from MLflow or local."""
        self._test_data_path = None

    @property
    def test_data_path(self):
        """Data path property getter."""
        # do i need to raise if self._data_path is uninitialized?
        return self._test_data_path

    @test_data_path.setter
    def test_data_path(self, path: str):
        """Data path property setter."""
        self._test_data_path = path

    @abstractmethod
    def predict_function(self):
        """Every model should make predictions."""
        raise NotImplementedError

    def upload_model(
        self,
        pyfunc_model_name: str,  # TODO weird argument, get rid of it
        artifacts: dict = None,
        registered_model_name: str = None,
    ):
        """Upload wrapper to MLmanagement server."""
        with mlmanagement.start_run(nested=True):
            mlmanagement.log_model(
                artifact_path=pyfunc_model_name,
                python_model=self,
                artifacts=artifacts,
                registered_model_name=self.model_name if hasattr(self, "model_name") else registered_model_name,
                action_type=ActionType.UPLOAD,  # should this be the same as job type? can also put it into class. OR, make it new type.
                source_model_name=self.source_model_name
                if hasattr(self, "source_model_name")
                else None,  # set that after model download from mlflow
                source_model_version=self.source_model_version
                if hasattr(self, "source_model_version")
                else None,  # set that after model download from mlflow
            )

    def set_experiment_name(self, experiment_name: str):
        """Set experiment name and return experiment."""
        mlmanagement.set_experiment(experiment_name)
        experiment = mlmanagement.get_experiment_by_name(experiment_name)
        return experiment

    @abstractmethod
    def get_data_flavour(self):
        """Every model is required to store one of the data flavour."""
        raise NotImplementedError
