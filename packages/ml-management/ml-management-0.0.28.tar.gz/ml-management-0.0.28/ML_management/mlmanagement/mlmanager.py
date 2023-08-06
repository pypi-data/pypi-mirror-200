"""This module create and send request to MLManagement server."""
import inspect
import json
import os
import shutil
from tempfile import TemporaryDirectory

import cloudpickle
import requests
from ML_management.mlmanagement.jsonschema_inference import infer_jsonschema
from ML_management.models.function_name_to_tag import FunctionNameToTag
from mlflow.exceptions import MlflowException, RestException
from requests_toolbelt import MultipartEncoder

import mlflow

need_active_run_functions = [
    "_add_eval_run",
    "start_run",
    "log_model",
    "log_metric",
    "set_tag",
    "autolog",
]

need_active_experiment_functions = ["set_experiment", "search_runs", "start_run"]

server_ml_api = os.environ.get("server_url", "http://localhost:8000") + "/mlflow"
is_server = os.environ.get("is_server", False)

active_run_stack = []
active_experiment_name = None


def create_kwargs(frame, is_it_class_function=False):
    """Get name and kwargs of function by its frame."""
    function_name = inspect.getframeinfo(frame)[2]  # get name of function
    _, _, _, kwargs = inspect.getargvalues(frame)  # get kwargs of function
    if is_it_class_function:
        del kwargs["self"]  # delete unneeded self arg
    return (
        function_name,
        kwargs,
    )  # return name of mlflow function and kwargs for that function


def request_log_model(function_name, kwargs, extra_attrs):
    """
    Send request for log_model function.

    Steps for log model:
    0) Infer jsonschema, raise if it is invalid
    1) open temporary directory
    2) Do mlflow.save_model() locally
    3) Pack it to zip file
    4) Send it to server to log model there.
    """
    delete_args_for_save_model_func = [
        "artifact_path",
        "registered_model_name",
        "await_registration_for",  # now, extra arguments
        "action_type",
        "source_model_name",
        "source_model_version",
    ]  # not need for save_model
    delete_args_for_log_func = [
        "python_model",
        "artifacts",
    ]  # not need for log model on server
    kwargs_for_save_model = kwargs.copy()
    for delete_arg in delete_args_for_save_model_func:
        del kwargs_for_save_model[delete_arg]

    python_model = kwargs_for_save_model["python_model"]
    # now we need to infer schemas for methods. We cannot check types of models,
    # because it leads to recursive imports.
    # TODO But if we only check method names, then user can inherit incorrectly
    # and still succeed! Should we make it more strict? How?!
    for func_name_to_infer in FunctionNameToTag:
        func_from_model = getattr(python_model, func_name_to_infer.name, None)
        if callable(func_from_model):
            function_schema = infer_jsonschema(func_from_model)
            kwargs[func_name_to_infer.value] = json.dumps(function_schema)

    with TemporaryDirectory() as temp_dir:
        model_folder = "model"
        path_for_model_folder = os.path.join(temp_dir, model_folder)
        zip_file_folder = "zip_file"
        path_for_zip_file = os.path.join(temp_dir, zip_file_folder)
        if kwargs["python_model"] is not None:
            mlflow.pyfunc.save_model(path=path_for_model_folder, **kwargs_for_save_model)

            for delete_arg in delete_args_for_log_func:
                del kwargs[delete_arg]
            kwargs["loader_module"] = mlflow.pyfunc.model.__name__
            model_filename = shutil.make_archive(path_for_zip_file, "zip", path_for_model_folder)

        elif kwargs["loader_module"] is not None:
            if not os.path.isdir(kwargs["data_path"]):
                raise Exception("Directory {0} doesn't exist".format(kwargs["data_path"]))
            model_filename = shutil.make_archive(path_for_zip_file, "zip", kwargs["data_path"])
        else:
            raise Exception("Either python_model or loader_module parameter must be specified")

        with open(model_filename, "rb") as file:
            return request(function_name, kwargs, extra_attrs, file)


def request(function_name, kwargs, extra_attrs, model_file, for_class=None):
    """Create mlflow_request and send it to server."""
    need_active_run = False
    if function_name in need_active_run_functions:
        need_active_run = True

    need_active_experiment = False
    if function_name in need_active_experiment_functions:
        need_active_experiment = True

    mlflow_request = {
        "function_name": function_name,
        "kwargs": kwargs,
        "for_class": for_class,
        "extra_attrs": extra_attrs,
        "experiment_name": active_experiment_name,
        "active_run_ids": list(map(lambda run: run.info.run_id, active_run_stack)),
        "need_active_run": need_active_run,
        "need_active_experiment": need_active_experiment,
    }
    files = {
        "mlflow_request": json.dumps(mlflow_request),
        "model_zip": ("filename", model_file, "multipart/form-data"),
    }

    multipart = MultipartEncoder(fields=files)
    return requests.post(server_ml_api, data=multipart, headers={"Content-Type": multipart.content_type})


def send_request_to_server(function_name, kwargs, extra_attrs, for_class):
    """
    Send request to server.

    Takes frame of mlflow func and extra_attr
    extra_attr is needed if original mlflow function is in the mlflow.<extra_attr> package
    for example function log_model is in mlflow.pyfunc module (mlflow.pyfunc.log_model())
    """
    # special case for log_model, load_model, save_model
    if function_name == "log_model":
        response = request_log_model(function_name, kwargs, extra_attrs)
    elif function_name == "load_model":
        return mlflow.pyfunc.load_model(**kwargs)
    elif function_name == "save_model":
        return mlflow.pyfunc.save_model(**kwargs)
    else:
        response = request(function_name, kwargs, extra_attrs, None, for_class)

    decoded_result = cloudpickle.loads(response.content)

    # raise error if mlflow is supposed to raise error
    if isinstance(decoded_result, MlflowException):
        is_rest = decoded_result.json_kwargs.pop("isRest", False)
        if is_rest:
            created_json = {
                "error_code": decoded_result.error_code,
                "message": decoded_result.message,
            }
            decoded_result = RestException(created_json)
        raise decoded_result
    elif isinstance(decoded_result, Exception):
        raise decoded_result
    return decoded_result


def request_for_function(frame, extra_attrs=None, for_class=None):
    """
    Send request to server or call mlflow function straightforward.

    Input parameters:
    :param frame: frame of equivalent mlflow function
    :param extra_attrs: list of extra modules for mlflow library, for example "tracking" (mlflow.tracking)
    :param for_class: parameters in case of mlflow class (for example mlflow.tracking.MLflowClient() class)
    """
    if extra_attrs is None:
        extra_attrs = []

    # Construct module for server case
    module = mlflow
    for extra_attr in extra_attrs:
        module = getattr(module, extra_attr)
    if for_class is not None:
        class_name = for_class["class_name"]
        kwargs_for_class = for_class["class_kwargs"]
        module = getattr(module, class_name)(**kwargs_for_class)
    function_name, kwargs = create_kwargs(frame, for_class is not None)
    # if that code is executed on server side - do mlflow function straightforward, else send request to server
    if is_server:
        return getattr(module, function_name)(**kwargs)
    else:
        return send_request_to_server(function_name, kwargs, extra_attrs, for_class)
