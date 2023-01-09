# PROJECT IMPORTS
import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config

from func.src.domain.validators.validator import ComplementaryData
from func.src.transports.device_info.transport import DeviceSecurity

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from func.main import complementary_data
                from func.src.services.jwt import JwtService
                from func.src.domain.enums.code import InternalCode
                from func.src.domain.response.model import ResponseModel
                from func.src.domain.exceptions.exceptions import (
                    OnboardingStepsStatusCodeNotOk,
                    InvalidOnboardingCurrentStep,
                    ErrorOnGetUniqueId,
                    InvalidNationality,
                    ErrorOnSendAuditLog,
                    ErrorOnDecodeJwt,
                    ErrorOnUpdateUser,
                    UserNotFound,
                    InvalidMaritalStatus,
                    InvalidOnboardingAntiFraud,
                    DeviceInfoRequestFailed,
                    DeviceInfoNotSupplied,
                )
                from func.src.services.validate_rules import ValidateRulesService
                from func.src.services.complementary_data import ComplementaryDataService

error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Unauthorized token",
    HTTPStatus.UNAUTHORIZED,
)
user_not_found_case = (
    UserNotFound(),
    UserNotFound.msg,
    InternalCode.DATA_NOT_FOUND,
    "Unexpected error occurred",
    HTTPStatus.UNAUTHORIZED,
)
onboarding_steps_status_code_not_ok_case = (
    OnboardingStepsStatusCodeNotOk(),
    OnboardingStepsStatusCodeNotOk.msg,
    InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
invalid_onboarding_current_step_case = (
    InvalidOnboardingCurrentStep("asd"),
    InvalidOnboardingCurrentStep.msg.format("asd"),
    InternalCode.ONBOARDING_STEP_INCORRECT,
    "User is not in correct step",
    HTTPStatus.BAD_REQUEST,
)
invalid_onboarding_anti_fraud_case = (
    InvalidOnboardingAntiFraud(),
    InvalidOnboardingAntiFraud.msg,
    InternalCode.ONBOARDING_STEP_INCORRECT,
    "User not approved",
    HTTPStatus.FORBIDDEN,
)
error_on_get_unique_id_case = (
    ErrorOnGetUniqueId(),
    ErrorOnGetUniqueId.msg,
    InternalCode.JWT_INVALID,
    "Fail to get unique_id",
    HTTPStatus.UNAUTHORIZED,
)
error_on_update_user_case = (
    ErrorOnUpdateUser(),
    ErrorOnUpdateUser.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
error_on_send_audit_log_case = (
    ErrorOnSendAuditLog(),
    ErrorOnSendAuditLog.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
invalid_marital_status_case = (
    InvalidMaritalStatus(),
    InvalidMaritalStatus.msg,
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST,
)
value_error_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST,
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
device_info_request_case = (
    DeviceInfoRequestFailed(),
    "Error trying to get device info",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Error trying to get device info",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
no_device_info_case = (
    DeviceInfoNotSupplied(),
    "Device info not supplied",
    InternalCode.INVALID_PARAMS,
    "Device info not supplied",
    HTTPStatus.BAD_REQUEST,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception,error_message,internal_status_code,response_message,response_status_code",
    [
        error_on_decode_jwt_case,
        user_not_found_case,
        onboarding_steps_status_code_not_ok_case,
        invalid_onboarding_current_step_case,
        error_on_get_unique_id_case,
        error_on_update_user_case,
        invalid_onboarding_anti_fraud_case,
        error_on_send_audit_log_case,
        invalid_marital_status_case,
        value_error_case,
        exception_case,
        device_info_request_case,
        no_device_info_case,
    ],
)
@patch.object(ComplementaryDataService, "update_user_with_complementary_data")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(ComplementaryData, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
@patch.object(DeviceSecurity, "get_device_info")
async def test_complementary_data_raising_errors(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_model,
    mocked_jwt_decode,
    mocked_logger,
    mocked_service,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await complementary_data()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(ComplementaryDataService, "update_user_with_complementary_data")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(ValidateRulesService, "__init__", return_value=None)
@patch.object(ValidateRulesService, "apply_validate_rules_to_proceed")
@patch.object(ComplementaryData, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
@patch.object(DeviceSecurity, "get_device_info")
async def test_complementary_data(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_model,
    mocked_validation_server_instance,
    mocked_validation,
    mocked_jwt_decode,
    mocked_logger,
    mocked_service,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await complementary_data()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=mocked_service.return_value,
        code=InternalCode.SUCCESS,
        message="User complementary data successfully updated",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
