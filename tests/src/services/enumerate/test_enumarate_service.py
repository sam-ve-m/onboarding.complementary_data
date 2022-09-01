# Jormungandr - Onboarding
from func.src.domain.exceptions.exceptions import (
    InvalidNationality,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
)

# Standard
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    return_value=True,
)
async def test_when_spouse_nationality_is_valid_then_return_true(
    mock_get_nationality, enumerate_service
):
    success = await enumerate_service._validate_nationality()

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    return_value=True,
)
async def test_when_spouse_is_none_then_return_true(
    mock_get_nationality, enumerate_service_only_mandatory
):
    success = await enumerate_service_only_mandatory._validate_nationality()

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    return_value=True,
)
async def test_when_spouse_nationality_is_valid_then_mock_was_called(
    mock_get_nationality, enumerate_service
):
    await enumerate_service._validate_nationality()

    mock_get_nationality.assert_called_once_with(nationality_code=5)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    return_value=False,
)
async def test_when_spouse_nationality_invalid_then_raises(
    mock_get_nationality, enumerate_service
):
    with pytest.raises(InvalidNationality):
        await enumerate_service._validate_nationality()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=True,
)
async def test_when_marital_status_is_valid_then_return_true(
    mock_get_marital_status, enumerate_service
):
    success = await enumerate_service._validate_marital_status()

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=None,
)
async def test_when_marital_status_invalid_then_raises(
    mock_get_marital_status, enumerate_service
):
    with pytest.raises(InvalidMaritalStatus):
        await enumerate_service._validate_marital_status()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_marital_status",
    return_value=True,
)
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_country",
    return_value=True,
)
@patch(
    "func.src.services.user_enumerate_data.EnumerateRepository.get_nationality",
    return_value=True,
)
async def test_when_all_valid_params_then_return_true(
    mock_nationality, mock_country, mock_marital, enumerate_service
):
    result = await enumerate_service.validate_enumerate_params()

    assert result is True
