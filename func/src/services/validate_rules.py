from ..domain.enums.types import UserOnboardingStep, UserAntiFraudStatus
from ..domain.exceptions.exceptions import (
    InvalidOnboardingCurrentStep,
    UserNotFound,
    InvalidSpouseCpf,
    InvalidOnboardingAntiFraud,
)
from ..domain.validators.validator import ComplementaryData
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.user_enumerate_data import EnumerateService
from ..transports.onboarding_steps.transport import OnboardingSteps


class ValidateRulesService:
    def __init__(self, payload_validated: ComplementaryData, jwt: str, unique_id: str):
        self.payload_validated = payload_validated
        self.jwt = jwt
        self.unique_id = unique_id

    async def validate_current_onboarding_step(self) -> bool:
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=self.jwt)
        if not user_current_step.step == UserOnboardingStep.COMPLEMENTARY_DATA:
            raise InvalidOnboardingCurrentStep(user_current_step.step)
        if user_current_step.anti_fraud == UserAntiFraudStatus.REPROVED:
            raise InvalidOnboardingAntiFraud()
        return True

    async def _get_user(self) -> dict:
        user = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user:
            raise UserNotFound()
        return user

    async def _validate_cpf_is_not_the_same(self) -> bool:
        user = await self._get_user()
        user_cpf = user["identifier_document"].get("cpf")
        if (
            bool(self.payload_validated.spouse)
            and self.payload_validated.spouse.cpf == user_cpf
        ):
            raise InvalidSpouseCpf()
        return True

    async def apply_validate_rules_to_proceed(self):
        enumerate_service = EnumerateService(
            complementary_data_validated=self.payload_validated
        )
        await enumerate_service.validate_enumerate_params()
        await self.validate_current_onboarding_step()
        await self._validate_cpf_is_not_the_same()
