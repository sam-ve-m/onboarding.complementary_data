# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.response.model import ResponseModel
from src.domain.validator import ComplementaryData
from src.services.jwt import JwtService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


async def user_complementary_data():
    jwt = request.headers.get("x-thebes-answer")
    raw_complementary_data = request.json
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    msg_error = "Unexpected error occurred"
    try:
        complementary_data_validated = ComplementaryData(**raw_complementary_data)
        success = True
        response = ResponseModel(
            success=success,
            message="User identifier data successfully updated",
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError:
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
