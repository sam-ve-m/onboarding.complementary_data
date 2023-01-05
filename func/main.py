from func.src.transports.device_info.transport import DeviceSecurity
from func.src.domain.exceptions.exceptions import (
    UserNotFound,
    ErrorOnUpdateUser,
    ErrorOnDecodeJwt,
    ErrorOnSendAuditLog,
    InvalidOnboardingCurrentStep,
    OnboardingStepsStatusCodeNotOk,
    ErrorOnGetUniqueId,
    InvalidNationality,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
    InvalidSpouseCpf,
    InvalidOnboardingAntiFraud,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.enums.code import InternalCode
from func.src.domain.response.model import ResponseModel
from func.src.domain.validators.validator import ComplementaryData
from func.src.services.jwt import JwtService
from func.src.services.validate_rules import ValidateRulesService
from func.src.services.complementary_data import ComplementaryDataService

from http import HTTPStatus

from etria_logger import Gladsheim
import flask


async def complementary_data() -> flask.Response:
    msg_error = "Unexpected error occurred"

    try:
        jwt = flask.request.headers.get("x-thebes-answer")
        encoded_device_info = flask.request.headers.get("x-device-info")
        raw_payload = flask.request.json

        payload_validated = ComplementaryData(**raw_payload)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        device_info = await DeviceSecurity.get_device_info(encoded_device_info)
        await ValidateRulesService(
            payload_validated=payload_validated, unique_id=unique_id, jwt=jwt
        ).apply_validate_rules_to_proceed()

        success = await ComplementaryDataService.update_user_with_complementary_data(
            unique_id=unique_id,
            payload_validated=payload_validated,
            device_info=device_info,
        )
        response = ResponseModel(
            success=success,
            message="User complementary data successfully updated",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Unauthorized token"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserNotFound as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.error(error=ex, message=ex.msg.format(str(ex)))
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="User is not in correct step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except InvalidOnboardingAntiFraud as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT.value,
            message="User not approved",
        ).build_http_response(status=HTTPStatus.FORBIDDEN)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except (
        InvalidMaritalStatus,
        InvalidCountryAcronym,
        InvalidNationality,
        InvalidSpouseCpf,
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except DeviceInfoRequestFailed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
