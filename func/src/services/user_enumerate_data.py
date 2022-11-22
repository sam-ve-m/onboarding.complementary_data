# Jormungandr
from ..domain.validators.validator import ComplementaryData
from ..domain.exceptions.exceptions import (
    InvalidNationality,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
)
from ..repositories.oracle.repository import EnumerateRepository


class EnumerateService:
    def __init__(self, complementary_data_validated: ComplementaryData):
        self.complementary_data = complementary_data_validated

    async def validate_enumerate_params(self) -> bool:
        await self._validate_nationality()
        await self._validate_marital_status()
        return True

    async def _validate_nationality(self) -> bool:
        spouse = self.complementary_data.spouse
        if not spouse:
            return True
        nationality_code = spouse.nationality
        result = await EnumerateRepository.get_nationality(
            nationality_code=nationality_code
        )
        if not result:
            raise InvalidNationality()
        return True

    async def _validate_marital_status(self) -> bool:
        marital_code = self.complementary_data.marital_status
        result = await EnumerateRepository.get_marital_status(marital_code=marital_code)
        if not result:
            raise InvalidMaritalStatus()
        return True
