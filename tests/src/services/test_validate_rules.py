from unittest.mock import patch, MagicMock

import pytest

from func.src.domain.enums.types import UserOnboardingStep, UserAntiFraudStatus
from func.src.domain.exceptions.exceptions import (
    InvalidOnboardingCurrentStep,
    InvalidOnboardingAntiFraud,
)
from func.src.services.validate_rules import ValidateRulesService
from func.src.transports.onboarding_steps.transport import OnboardingSteps

dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step_invalid_step(mocked_transport):
    mocked_transport.return_value.step = None
    with pytest.raises(InvalidOnboardingCurrentStep):
        await ValidateRulesService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value.jwt)


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step_invalid_anti_fraud(mocked_transport):
    mocked_transport.return_value.step = UserOnboardingStep.COMPLEMENTARY_DATA
    mocked_transport.return_value.anti_fraud = UserAntiFraudStatus.REPROVED
    with pytest.raises(InvalidOnboardingAntiFraud):
        await ValidateRulesService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value.jwt)


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step(mocked_transport):
    mocked_transport.return_value.step = UserOnboardingStep.COMPLEMENTARY_DATA
    mocked_transport.return_value.anti_fraud = None
    result = await ValidateRulesService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value.jwt)
    assert result is True
