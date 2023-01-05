# Jormungandr - Onboarding
from func.src.domain.complementary_data.model import ComplementaryDataModel
from func.src.domain.exceptions.exceptions import (
    UserNotFound,
    InvalidSpouseCpf,
    ErrorOnUpdateUser,
    InvalidOnboardingCurrentStep,
)
from func.src.services.complementary_data import ComplementaryDataService
from func.src.services.validate_rules import ValidateRulesService
from func.src.transports.onboarding_steps.transport import OnboardingSteps
from tests.src.services.complementary_data.stubs import (
    stub_unique_id,
    stub_user,
    stub_user_same_cpf,
    stub_user_updated,
    stub_user_not_updated,
    stub_device_info,
)

# Standard
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.find_one_by_unique_id",
    return_value={"stub": "stub"},
)
async def test_when_get_valid_user_then_return_user(mock_get_user, comp_data_service):
    user = await comp_data_service._get_user()

    assert isinstance(user, dict)


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.find_one_by_unique_id",
    return_value={"stub": "stub"},
)
async def test_when_get_valid_user_then_mock_was_called(
    mock_get_user, comp_data_service
):
    await comp_data_service._get_user()

    mock_get_user.assert_called_once_with(unique_id=stub_unique_id)


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.find_one_by_unique_id",
    return_value=None,
)
async def test_when_get_valid_user_then_raises(mock_get_user, comp_data_service):
    with pytest.raises(UserNotFound):
        await comp_data_service._get_user()


@pytest.mark.asyncio
@patch.object(ValidateRulesService, "_get_user", return_value=stub_user)
async def test_when_valid_cpf_spouse_then_return_true(mock_get_user, comp_data_service):
    success = await comp_data_service._validate_cpf_is_not_the_same()

    assert success is True


@pytest.mark.asyncio
@patch.object(ValidateRulesService, "_get_user", return_value=stub_user)
async def test_when_valid_cpf_spouse_then_mock_was_called(
    mock_get_user, comp_data_service
):
    await comp_data_service._validate_cpf_is_not_the_same()

    mock_get_user.assert_called_once_with()


@pytest.mark.asyncio
@patch.object(ValidateRulesService, "_get_user", return_value=stub_user_same_cpf)
async def test_when_same_cpf_user_then_raises(mock_get_user, comp_data_service):
    with pytest.raises(InvalidSpouseCpf):
        await comp_data_service._validate_cpf_is_not_the_same()


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.update_one_with_user_complementary_data",
    return_value=stub_user_updated,
)
@patch("func.src.services.complementary_data.Audit.record_message_log")
@patch.object(ValidateRulesService, "_validate_cpf_is_not_the_same")
async def test_when_update_user_success_then_return_true(
    mock_validate_cpf, mock_audit, mock_update, comp_data_service
):
    success = await ComplementaryDataService.update_user_with_complementary_data(
        comp_data_service.payload_validated,
        comp_data_service.unique_id,
        stub_device_info,
    )

    assert success is True


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.update_one_with_user_complementary_data",
    return_value=stub_user_updated,
)
@patch("func.src.services.complementary_data.Audit.record_message_log")
async def test_when_update_user_success_then_mock_was_called(
    mock_audit, mock_update, comp_data_service
):
    await ComplementaryDataService.update_user_with_complementary_data(
        comp_data_service.payload_validated,
        comp_data_service.unique_id,
        stub_device_info,
    )
    complementary_data_model = ComplementaryDataModel(
        payload_validated=comp_data_service.payload_validated,
        unique_id=comp_data_service.unique_id,
        device_info=stub_device_info,
    )
    user_complementary_data = await complementary_data_model.get_user_update_template()

    mock_audit.assert_called_once()
    mock_update.assert_called_once_with(
        unique_id=stub_unique_id, user_complementary_data=user_complementary_data
    )


@pytest.mark.asyncio
@patch(
    "func.src.services.complementary_data.UserRepository.update_one_with_user_complementary_data",
    return_value=stub_user_not_updated,
)
@patch("func.src.services.complementary_data.Audit.record_message_log")
@patch.object(ValidateRulesService, "_validate_cpf_is_not_the_same")
async def test_when_update_user_fail_then_raises(
    mock_validate_cpf, mock_audit, mock_update, comp_data_service
):
    with pytest.raises(ErrorOnUpdateUser):
        await ComplementaryDataService.update_user_with_complementary_data(
            comp_data_service.payload_validated,
            comp_data_service.unique_id,
            stub_device_info,
        )
