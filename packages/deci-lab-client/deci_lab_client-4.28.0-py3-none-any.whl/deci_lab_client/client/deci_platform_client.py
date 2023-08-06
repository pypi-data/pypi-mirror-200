import getpass
import io
import logging
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from typing import TYPE_CHECKING
from warnings import warn

import jwt
import requests
from cryptography.fernet import Fernet, InvalidToken
from deci_common.abstractions.abstract_logger import get_logger
from deci_lab_client.api.platform_api import PlatformApi
from deci_lab_client.api_client import ApiClient
from deci_lab_client.client.exceptions import (
    InvalidAuthenticationTokenError,
    NotLoggedInError,
    PremiumOnlyFeatureError,
    PyTorchNotInstalledError,
    TimeoutWasReachedBeforeBenchmarkFinishedError,
    UnsupportedLoadedModelFramework,
)
from deci_lab_client.client.helpers import (
    TqdmUpTo,
    build_gru_request_form,
    build_model_metadata,
    wait_until,
)
from deci_lab_client.configuration import Configuration
from deci_lab_client.exceptions import ApiException
from deci_lab_client.models import (
    AddModelResponse,
    APIResponse,
    BodyAddModelV2,
    ExperimentForm,
    FrameworkType,
    LogRequestBody,
    ModelBenchmarkState,
    ModelMetadata,
    ModelSource,
    OptimizationRequestForm,
    OptimizeModelResponse,
    SentryLevel,
)
from deci_lab_client.types.s3_signed_url import S3SignedUrl
from jwt.exceptions import ExpiredSignatureError
from requests import Response

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence
    from typing import Any, Optional
    from uuid import UUID

    from deci_lab_client.models import (
        APIResponseAddModelResponse,
        BaselineModelResponseMetadata,
    )
    from torch import nn

BEARER_TYPE = "Bearer"
ENCRYPT_KEY = b"VSyHy9dIgVpdZo03eG0XR0J8RJh6t1vX7BNXkt2WANo="
f_encryptor = Fernet(ENCRYPT_KEY)


def get_docstring_from(original_function):
    """
    A decorator that attaches the docstring one function to another function in real time
    (for transparent auto completion).
    """

    def doc_wrapper(target):
        target.__doc__ = original_function.__doc__
        return target

    return doc_wrapper


class AddAndOptimizeResponse:
    def __init__(
        self,
        model_id: "Optional[UUID]" = None,
        benchmark_request_id: "Optional[UUID]" = None,
        optimized_model_id: "Optional[UUID]" = None,
        optimization_request_id: "Optional[UUID]" = None,
    ):
        self.model_id = model_id
        self.benchmark_request_id = benchmark_request_id
        self.optimized_model_id = optimized_model_id
        self.optimization_request_id = optimization_request_id


class DeciPlatformClient(PlatformApi):
    """
    A wrapper for OpenAPI's generated client http library to deci's API.
    Extends the functionality of generated platform client and ease it's usage and experience.
    """

    TOKEN_PATH = f"{os.path.join(os.path.expanduser('~'), '.deci/auth/token')}"

    @staticmethod
    def _token_path_exists():
        return os.path.isfile(DeciPlatformClient.TOKEN_PATH)

    @staticmethod
    def _create_token_path_if_missing():
        if not DeciPlatformClient._token_path_exists():
            Path(os.path.dirname(DeciPlatformClient.TOKEN_PATH)).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_local_auth_token():
        if DeciPlatformClient._token_path_exists():
            try:
                with open(DeciPlatformClient.TOKEN_PATH, "rb") as file:
                    encrypted_text = file.read()
                    return f_encryptor.decrypt(encrypted_text).decode()
            except Exception:
                raise InvalidAuthenticationTokenError(
                    "Bad authentication token. Please log in to Deci lab in order to generate a new token"
                )
        return None

    def _append_auth_token_to_headers(self, auth_token):
        self.api_client.default_headers["Authorization"] = f"{BEARER_TYPE} {auth_token}"

    def __init__(self, api_host="api.deci.ai", api_port=443, https=True, proxy=None, proxy_headers=None, logger=None):
        """
        :param api_host: The host of deci's platform HTTP API.
        :type api_host: str
        :param api_host: The port of deci's platform HTTP API.
        :type api_port: int
        :param https: Whether to use https instead of HTTP. Using https Will add latency.
        :type https: bool
        """
        self._logger = logger or get_logger(logger_name="deci_platform_client")
        assert isinstance(api_port, int), "The api_port must be an int object"
        endpoint_host = "{api_host}:{api_port}".format(api_host=api_host, api_port=api_port)

        if https:
            base_url = "https://{endpoint}".format(endpoint=endpoint_host)
        else:
            base_url = "http://{endpoint}".format(endpoint=endpoint_host)

        if proxy is None:
            proxy = os.getenv("DECI_CLIENT_PROXY_URL")

        configuration = Configuration(host=base_url)
        configuration.proxy = proxy
        configuration.proxy_headers = proxy_headers
        client_config = ApiClient(configuration=configuration)
        super().__init__(client_config)

        self._token_data: "Optional[dict[str, Any]]" = None
        self._api_host = api_host
        self._endpoint_host = endpoint_host
        self._base_url = base_url

        self.experiment = None
        self.experiments_pool: "dict[str, threading.Thread]" = dict()
        try:
            local_token = os.getenv("DECI_PLATFORM_TOKEN") or DeciPlatformClient._get_local_auth_token()
            valid, token = self.verify_token_exp(token=local_token)
        except InvalidAuthenticationTokenError:
            self._logger.error(
                "Your authentication token is invalid. Please visit https://console.deci.ai/settings for your token."
            )
        else:
            if valid:
                self._append_auth_token_to_headers(token)
                self._logger.info(
                    "Your Current session is valid. If you wish to login with another user call logout on the client"
                )

    @property
    def _is_premium(self) -> bool:
        token_data = self._token_data if self._token_data is not None else {}
        return token_data.get("is_premium", False)

    def verify_token_exp(self, token: "Optional[str]") -> "tuple[bool, Optional[str]]":
        """
        Checks the JWT token validity. If a token param is not provided it attempts to validate the currently stored
        token
        :param token:  A token obtained from the user settings page in the Lab
        :type token: str
        """
        if token:
            try:
                if token.index(" ") == 0:
                    self._logger.info("Please provide a token without its type")
                    return False, None
            except ValueError:
                # This means that the token format does not include bearer/Bearer which is the desired behavior.
                pass
        else:
            return False, None

        try:
            self._token_data = jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
        except ExpiredSignatureError:
            self._logger.error(
                "It seems your authentication token has expired, Please login with your regular credentials first. You \
                may as well log in to the Platform UI and copy your token from the settings page [https://console.deci.ai/settings]."
            )
            return False, None

        return True, token

    def _store_auth_token(self, auth_token: str, persist_locally):
        self._append_auth_token_to_headers(auth_token)
        if persist_locally:
            DeciPlatformClient._create_token_path_if_missing()
            self._logger.warning(
                "Turn off the store_token flag on non safe environments or"
                f" remove {DeciPlatformClient.TOKEN_PATH} after the use."
            )
            encrypted_text = f_encryptor.encrypt(auth_token.encode())
            with open(DeciPlatformClient.TOKEN_PATH, "wb") as file:
                file.write(encrypted_text)

    def _login_with_user_credentials(self, username: str, password: str, store_token: bool):
        if not username or not password:
            username = username or input("Email: ")
            password = password or getpass.getpass()

        response = super(DeciPlatformClient, self).login(username, password)
        self._store_auth_token(auth_token=response.access_token, persist_locally=store_token)

    def login(self, username: str = None, password: str = None, token: str = None, store_token: bool = True):
        """
        Login to the platform.
        Provides a mechanism to log in to the Deci lab. A previously generated token can be provided and in such case
        the username and password won't be necessary (the token will be verified). A new token will be requested if both
        the username and password are provided. If neither a token, username and password is provided a check for a
        local token will be executed

        :param username: The user email which was used to register in the Deci lab
        :type username: str
        :param password: The user password provided upon account creation in Deci lab.
        :type password: str
        :param token: A token provided by Deci lab
        :type token: str
        :param store_token: By default when you use your credentials, a token will be saved on your machine to allow
            future auto-login.
        :type store_token: bool
        IMPORTANT: turn off the store_token flag on non safe environments.
        """

        force_login = bool(username or password)
        token_valid, token_str = self.verify_token_exp(token=token)
        try:
            if force_login:
                self._login_with_user_credentials(username=username, password=password, store_token=store_token)
            elif token_valid:
                self._store_auth_token(auth_token=token_str, persist_locally=store_token)
            else:
                self._logger.info("No parameter was provided. We'll search for a token stored locally")
                local_token = DeciPlatformClient._get_local_auth_token()
                valid, token = self.verify_token_exp(token=local_token)
                if valid:
                    self._append_auth_token_to_headers(token)
                    self._logger.info("A local token was found and it contains a valid signature")
                elif not token:
                    self._logger.info("A local token was not found. Please log in with your Deci lab credentials")
                    self._login_with_user_credentials(username=username, password=password, store_token=store_token)
        except InvalidToken:
            raise InvalidAuthenticationTokenError(
                "It seems your authentication token is not valid or has been expired, Please login with your regular \n"
                "credentials first."
            )

        self._logger.info("Successfully logged in to the platform.")

    def logout(self):
        """
        Log out of the platform (Disposes the credentials).
        """
        try:
            self.api_client.default_headers.pop("Authorization")
        except KeyError:
            pass
        self._token_data = None
        if DeciPlatformClient._token_path_exists():
            os.remove(DeciPlatformClient.TOKEN_PATH)
        self._logger.info("Successfully logged out.")

    def _prepare_model(
        self,
        model_metadata: "ModelMetadata",
        model: "Optional[nn.Module]",
        **kwargs: "Any",
    ) -> "Optional[str]":
        model_path: "Optional[str]" = None
        if model is not None:
            if model_metadata.framework == FrameworkType.PYTORCH:
                with self.support(tag="pytorch-to-onnx"):
                    model_path = self.convert_pytorch_to_onnx(
                        local_loaded_model=model,
                        primary_batch_size=model_metadata.primary_batch_size,
                        input_dimensions=model_metadata.input_dimensions,
                        **kwargs,
                    )
                model_metadata.framework = FrameworkType.ONNX
            else:
                raise UnsupportedLoadedModelFramework
        model_metadata.source = ModelSource.SDK
        self.assert_model_arguments(model_metadata=model_metadata)
        return model_path

    def _add_model_start(
        self,
        model_metadata: "ModelMetadata",
        model: "Optional[nn.Module]" = None,
        model_path: "Optional[str]" = None,
        **kwargs: "Any",
    ) -> "str":
        if (model is not None and model_path is not None) or (model is None and model_path is None):
            raise TypeError(
                f"Exactly one of model and model_path parameters must be specified,"
                f" received model={model}, model_path={model_path}"
            )

        converted_pytorch_model_path = self._prepare_model(model_metadata=model_metadata, model=model, **kwargs)

        self.assert_model_arguments(model_metadata=model_metadata)
        storage_etag = self._upload_file_to_s3(
            converted_pytorch_model_path if converted_pytorch_model_path is not None else model_path,
            model_metadata.name,
        )

        if converted_pytorch_model_path is not None:
            try:
                os.remove(converted_pytorch_model_path)
            except (OSError, UnboundLocalError):
                pass

        return storage_etag

    def add_model_v2(
        self,
        model_metadata: "ModelMetadata",
        hardware_types: "list[str]",
        model_path: "Optional[str]" = None,
        model: "Optional[nn.Module]" = None,
        **kwargs: "Any",
    ):
        """
        Adds a new model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        For pytorch model is expected, for other framework use model_local path instead.
        :param model_metadata: The model metadata.
        :param hardware_types: The hardware types you want to benchmark the model on.
        :param model_path: The path of the model on the local operating system.
        :param model: Pytorch loaded model object.
        if your model's framework is pytorch you may pass the following parameters as kwargs
            in order to control the conversion to onnx:
        :param kwargs: Extra arguments to be passed to the PyTorch to ONNX conversion, for example:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        storage_etag = self._add_model_start(
            model_metadata=model_metadata,
            model=model,
            model_path=model_path,
            **kwargs,
        )
        return super(DeciPlatformClient, self).add_model_v2(
            etag=storage_etag,
            body_add_model_v2=BodyAddModelV2(model=model_metadata, hardware_types=hardware_types),
        )

    def add_pytorch_model(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        hardware_types: "list[str]",
        channel_first=True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        **kwargs: "Any",
    ):
        """
        Adds a new PyTorch model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param hardware_types: A list of hardware types to benchmark the model on.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        model_metadata = build_model_metadata(
            name=name,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=hardware_types,
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
        )
        kwargs.pop("model_metadata", None)

        return self.add_model_v2(model_metadata=model_metadata, hardware_types=hardware_types, model=model, **kwargs)

    def add_and_optimize_pytorch_model(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        hardware_types: "list[str]",
        channel_first=True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        primary_batch_size: int,
        quantization_level: str,
        raw_format=False,
        **kwargs: "Any",
    ):
        """
        Adds a new PyTorch model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param hardware_types: A list of hardware types to benchmark the model on.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param primary_batch_size: The model's primary batch size. Optional.
                                   Allowed values can be seen in deci_lab_client.BatchSize
                                   and deci_lab_client.BatchSize.
        :param quantization_level: The quantization level to optimize for. Optional.
                                   Allowed values can be seen in deci_lab_client.QuantizationLevel.
        :param raw_format: Whether the optimized model should be saved in raw format or not. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        add_model_response: "APIResponseAddModelResponse" = self.add_pytorch_model(
            model,
            name=name,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=hardware_types,
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
            **kwargs,
        )
        model_id = add_model_response.data.model_id
        return self.gru_model(
            model_id=model_id,
            gru_request_form=build_gru_request_form(
                batch_size=primary_batch_size,
                quantization_level=quantization_level,
                target_hardware_types=hardware_types,
                raw_format=raw_format,
            ),
        )

    def add_pytorch_architecture(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        primary_hardware_type: str,
        primary_batch_size: int,
        quantization_level: str,
        channel_first=True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        dataset_name: "Optional[str]" = None,
        target_metric: "Optional[str]" = None,
        target_metric_value: "Optional[float]" = None,
        model_size: "Optional[float]" = None,
        memory_footprint: "Optional[float]" = None,
        raw_format=False,
        **kwargs: "Any",
    ):
        """
        Adds a new PyTorch architecture to the company's model repository, using the new v2 endpoint,
        and requesting an AutoNAC optimization on that model.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param primary_hardware_type: The primary hardware type to benchmark the model and create the AutoNAC model on.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param dataset_name: The name of a similar dataset to that your model was trained on. Optional.
        :param target_metric: The AutoNAC model's target metric. Optional.
                              Allowed values can be seen in deci_lab_client.Metric.
        :param target_metric_value: The AutoNAC model's target metric value. Optional.
        :param model_size: The AutoNAC model's target model size. Optional.
        :param memory_footprint: The AutoNAC model's target memory footprint. Optional.
        :param primary_batch_size: The model's primary batch size. Optional, defaults to 1.
                                   Allowed values can be seen in deci_lab_client.BatchSize
                                   and deci_lab_client.BatchSize.
        :param quantization_level: The quantization level to optimize for. Optional, defaults to FP16.
                                   Allowed values can be seen in deci_lab_client.QuantizationLevel.
        :param raw_format: Whether the optimized model should be saved in raw format or not. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        if not self._is_premium:
            raise PremiumOnlyFeatureError

        model_metadata = build_model_metadata(
            name=name,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=[primary_hardware_type],
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
            dataset_name=dataset_name,
            target_metric=target_metric,
            target_metric_value=target_metric_value,
            model_size=model_size,
            memory_footprint=memory_footprint,
        )
        kwargs.pop("model_metadata", None)

        add_model_response: "APIResponseAddModelResponse" = self.add_model_v2(
            model_metadata=model_metadata,
            hardware_types=[primary_hardware_type],
            model=model,
            **kwargs,
        )
        model_id = add_model_response.data.model_id
        self.autonac_model(model_id=model_id)
        return self.gru_model(
            model_id=model_id,
            gru_request_form=build_gru_request_form(
                batch_size=primary_batch_size,
                quantization_level=quantization_level,
                target_hardware_types=[primary_hardware_type],
                target_metric=target_metric,
                raw_format=raw_format,
            ),
        )

    def add_model(
        self,
        add_model_request: ModelMetadata,
        optimization_request: OptimizationRequestForm = None,
        model_local_path: str = None,
        local_loaded_model=None,
        wait_async=False,
        **kwargs,
    ):
        """
        DEPRECATED
        Adds a new model to the company's model repository.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        For pytorch local_loaded_model is expected, for other framework use model_local path instead.
        :param add_model_request: The model metadata
        :param optimization_request: The params to due optimize the model, if not given model will not be optimized. You can always request the optimization later.
        :param model_local_path: The path of the model on the local operating system.
        :param local_loaded_model: Pytorch loaded model object.
        :param wait_async: If true function will wait unitl the benchmark process was finished, otherwise will return on request acknowledgement.
        if your model's framework is pytorch you may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        :param dynamic_axes
        :param input_names
        :param output_names
        """
        warn("This method is deprecated, please migrate to using the new 'add_model_v2' method")
        s3_file_etag = self._add_model_start(
            model_metadata=add_model_request,
            model=local_loaded_model,
            model_path=model_local_path,
            **kwargs,
        )

        try:
            # Adding the model metadata via the API, after verification that the file exists.
            add_model_response: AddModelResponse = super(DeciPlatformClient, self).add_model(
                model_metadata=add_model_request, etag=s3_file_etag, **kwargs
            )
            response = AddAndOptimizeResponse(**add_model_response.data.to_dict())
            new_model_id = add_model_response.data.model_id
            if wait_async and not optimization_request:
                return_value = wait_until(
                    self._wait_for_benchmark_to_finish, 20 * 60, optimized_model_id=str(new_model_id)
                )
                if not return_value:
                    raise TimeoutWasReachedBeforeBenchmarkFinishedError
        except Exception as ex:
            self._logger.error(f"Failed to add the model to the repository. {ex}")
            raise ex
        else:
            self._logger.info("Successfully added the model to the repository.")
            self._logger.info(
                "Starting to benchmark the model on the required hardware types. "
                f"You can check the status on https://console.deci.ai/insights/{response.model_id} or by querying the platform."
            )
        if not optimization_request:
            return APIResponse(success=True, message=add_model_response.message, data=response)
        # Requesting to optimize the added model metadata via the API.
        optimize_model_response: OptimizeModelResponse = super(DeciPlatformClient, self).optimize_model(
            model_id=new_model_id, optimization_request_form=optimization_request, **kwargs
        )
        response_dict = response.__dict__
        response_dict.update(optimize_model_response.data.to_dict())
        response = AddAndOptimizeResponse(**response_dict)
        if wait_async:
            return_value = wait_until(
                self._wait_for_benchmark_to_finish, 20 * 60, model_id=str(response.optimized_model_id)
            )
            if return_value:
                self._logger.info(
                    f"Successfully added and optimized {str(return_value.name)} on your model repository. "
                    f"You can see the benchmark results at https://console.deci.ai/insights/{add_model_response.data.model_id}/optimized/{optimize_model_response.data.optimized_model_id}"
                )
            else:
                raise TimeoutWasReachedBeforeBenchmarkFinishedError

        return APIResponse(
            success=True,
            message="Successfully added the model to the model repository and optimized it. ",
            data=response,
        )

    def download_model(self, model_id: str, dest_path: "Optional[str]" = None, show_progress=True) -> Path:
        """
        Downloads a model with the specified UUID to the specified path.
        :param model_id: The model UUID
        :param dest_path: The full path to which the model will be written to, will download to current working directory if None supplied
        :param show_progress: Whether to show the current progress of download
        :return path to the downloaded model
        """
        download_url = self.get_model_signed_url_for_download(model_id=model_id)
        if not dest_path:
            filename = re.findall('filename="(.+)"&', urllib.parse.unquote(download_url.data))[0]
            dest_path = Path.cwd().joinpath(filename)
        self._logger.info("Downloading...")
        with TqdmUpTo(**TqdmUpTo.DOWNLOAD_PARAMS, desc=str(dest_path)) as t:
            urllib.request.urlretrieve(
                url=download_url.data, filename=dest_path, reporthook=t.update_to if show_progress else None
            )
        self._logger.info(f"The model was downloaded to {dest_path}")
        return dest_path

    def _all_models(self) -> "list[ModelMetadata]":
        models = self.get_all_models()
        return [model for model in models.data if not model.deleted]

    def find_model_id(self, model_name: str) -> ModelMetadata:
        return next((model for model in self._all_models() if model.name == model_name), None)

    @staticmethod
    @contextmanager
    def redirect_output() -> "Generator[tuple[io.StringIO, io.StringIO], Any, None]":
        root_logger = logging.getLogger()
        logs = io.StringIO()
        handler = logging.StreamHandler(logs)
        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)
        with redirect_stdout(io.StringIO()) as stdout:
            yield stdout, logs

        root_logger.removeHandler(handler)

    def send_support_logs(
        self,
        *,
        log: str,
        tag: "Optional[str]" = None,
        level: "Optional[SentryLevel]" = None,
    ) -> None:
        if not self._token_data:
            raise NotLoggedInError
        if not self._is_premium:
            raise PremiumOnlyFeatureError
        if len(log) == 0:
            self._logger.info("No logs detected, not sending anything.")
            return
        log_request_body = LogRequestBody(log=log, tag=tag, level=level)
        self.log(log_request_body=log_request_body)
        self._logger.info("Successfully sent support logs.")

    @contextmanager
    def support(
        self,
        tag: "Optional[str]" = None,
        level: "Optional[SentryLevel]" = None,
    ) -> "Generator[None, None, Any]":
        exception: "Optional[Exception]" = None
        with self.redirect_output() as (stdout, logs):
            try:
                yield
            except Exception as e:
                exception = e
        log = "\n".join(["stdout:", stdout.getvalue(), "logging:", logs.getvalue()])
        if self._is_premium:
            self.send_support_logs(log=log, tag=tag, level=level)
        if exception is not None:
            raise exception

    @staticmethod
    def convert_pytorch_to_onnx(
        local_loaded_model: "nn.Module",
        primary_batch_size: int,
        input_dimensions: "Sequence[int]",
        export_path: "Optional[str]" = None,
        opset_version=15,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},  # Variable length axes
        **kwargs: "Any",
    ) -> str:
        """
        Convert PyTorch model to ONNX.
        :param local_loaded_model: Pytorch loaded model object (nn.Module).
        :param primary_batch_size: The batch_size for your model
        :param input_dimensions: The input dims of the model. ex:(3, 224, 224)
        :param export_path: Path to where to save the converted model file.
            If not given "converted_model_{time.time()}.onnx" will be used.

        You may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        :param dynamic_axes
        :param input_names
        :param output_names
        """
        try:
            import torch
        except Exception as e:
            raise PyTorchNotInstalledError from e
        # Input to the model
        model_input = torch.randn(primary_batch_size, *input_dimensions, requires_grad=False)
        model_path = export_path if export_path is not None else f"converted_model_{time.time()}.onnx"

        # Export the model
        local_loaded_model.eval()  # Put model into eval mode
        if hasattr(local_loaded_model, "prep_model_for_conversion"):
            local_loaded_model.prep_model_for_conversion(input_size=input_dimensions)

        logging.info(f"Running torch.jit.trace on model with input dimensions {input_dimensions}")
        try:
            local_loaded_model = torch.jit.trace(local_loaded_model, model_input)
            logging.info("Successfully traced model.")
        except torch.jit.TracingCheckError as e:
            logging.error("Error tracing model")
            logging.error(e)

        logging.info(f"Exporting model to ONNX with opset version {opset_version}")
        try:
            torch.onnx.export(
                local_loaded_model,  # Model being run
                model_input,  # a torch tensor contains the model input dims and the primary_batch_size.
                model_path,  # Where to save the model (can be a file or file-like object)
                export_params=True,  # Store the trained parameter weights inside the model file
                opset_version=opset_version,  # The ONNX version to export the model to
                do_constant_folding=do_constant_folding,  # Whether to execute constant folding for optimization
                input_names=input_names,  # The model's input names
                output_names=output_names,  # The model's output names
                dynamic_axes=dynamic_axes,
                **kwargs,
            )
        except Exception as e:
            logging.error("Error converting model")
            logging.error(e)
            raise
        logging.info("Successfully exported model")

        return model_path

    def _wait_for_benchmark_to_finish(self, model_id: str):
        your_model_from_repo = self.get_model_by_id(model_id=model_id).data
        if your_model_from_repo.benchmark_state not in [ModelBenchmarkState.IN_PROGRESS, ModelBenchmarkState.PENDING]:
            return your_model_from_repo
        return False

    def _upload_file_to_s3(self, model_local_path: str, model_name: str, model_version: "Optional[str]" = None):
        with open(model_local_path, "rb") as f:
            # Upload the model to the s3 bucket of the company
            signed_url_upload_request = self.get_model_signed_url_for_upload(
                model_name=model_name, model_version=model_version
            )
            upload_request_parameters = signed_url_upload_request.data
            requests.post(upload_request_parameters["url"], data=[])
            self._logger.info("Uploading the model file...")
            files = {"file": (upload_request_parameters["fields"]["key"], f)}
            http_response = requests.post(
                upload_request_parameters["url"], data=upload_request_parameters["fields"], files=files
            )
            # Getting the s3 created Etag from the http headers, and passing it to the 'add_model' call
            s3_file_etag = http_response.headers.get("ETag")  # Verify the model was uploaded
            http_response.raise_for_status()
            self._logger.info("Finished uploading the model file.")
            return s3_file_etag

    # TODO: Make the above method to use the one that follows. Ensure good naming conventions.
    @staticmethod
    def upload_file_to_s3(from_path: str, s3_signed_url: S3SignedUrl) -> Response:
        with open(from_path, "rb") as file:
            files = {"file": (s3_signed_url.fields["key"], file)}
            http_response = requests.post(s3_signed_url.url, files=files, data=s3_signed_url.fields)
            return http_response

    def register_experiment(self, name: str, model_name: "Optional[str]" = None, resume: bool = True) -> None:
        """
        Registers a training experiment in Deci's backend

        :param name: The experiment name
        :param model_name: The model name that being run in the experiment. Optional.
        :param resume: Resume the experiment `name` by uploading files to the existing experiment folder alongside any existing files.
                       If `resume=False` - archive all previously existing experiment `name` files. True by default.
        """
        try:
            response = self.start_experiment(
                experiment_form=ExperimentForm(name=name, model_name=model_name, resume=resume)
            )
            if not response.success:
                raise ApiException

            self.experiment = response.data
        except Exception:
            self._logger.error(f"Failed to register experiment {name}")

    def save_experiment_file(self, file_path: str) -> "threading.Thread":
        """
        Uploads a training related file to Deci's location in S3. This can be a TensorBoard file or a log

        :param file_path: The local path of the file to be uploaded
        """

        def save(path: str, existing_thread: "Optional[threading.Thread]") -> None:
            # If there's already an upload schedule for the same file kill it
            if existing_thread:
                self._logger.debug("There's already a thread trying to upload the same filename")
                existing_thread.join()
                self._logger.debug("Old thread finished. We'll create a new one")

            if not os.path.exists(path):
                self._logger.warning("We didn't find that file")
                return

            try:
                filename = os.path.basename(file_path)
                response = self.get_experiment_upload_url(
                    experiment_id=self.experiment.id,
                    filename=filename,
                    model_id=self.experiment.model_id,
                )
            except Exception:
                self._logger.error("We couldn't fetch an upload URL from the server")
                return

            try:
                s3_target = S3SignedUrl(**response.data)
                upload_response = self.upload_file_to_s3(from_path=file_path, s3_signed_url=s3_target)
                upload_response.raise_for_status()
            except Exception:
                self._logger.error("We couldn't upload your file")

        file_absolute_path = str(Path(file_path).resolve())
        current_thread = self.experiments_pool.get(file_absolute_path)

        save_file_thread = threading.Thread(target=save, args=(file_absolute_path, current_thread))
        self.experiments_pool[file_absolute_path] = save_file_thread

        save_file_thread.start()
        return save_file_thread

    def get_model(
        self, name: "str", version: "Optional[str]" = None, download_path: "Optional[str]" = None, should_download=True
    ) -> "tuple[BaselineModelResponseMetadata, Optional[Path]]":
        """
        Get a model from the user's model repository in Lab tab, and optionally downloads the model file to the local machine
        :param name: Name of the model to retrieve from the lab
        :param version: Version of the model to retrieve from the lab (the version is specified near the model name)
        :param download_path: An optional download path to download the model to, if not supplied and should_download is set to True, will download to the current working directory
        :param should_download: A flag to indicate whether to download the model's file locally, defaults to False.
        :return: a tuple containing the model metadata and the download path (or None, if not downloaded) for the location of the model in the local machine
        """

        model_metadata = self.get_model_by_name(name=name, version=version).data
        if should_download:
            download_path = self.download_model(model_id=model_metadata.model_id, dest_path=download_path)
        return model_metadata, download_path
