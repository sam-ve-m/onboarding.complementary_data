from ..repositories.oracle.repository import EnumerateRepository
from ..domain.exceptions import InvalidNationality, InvalidMaritalStatus, InvalidCountryAcronym


class EnumerateService:
    def __init__(self, complementary_data_validated: dict):
        self.complementary_data = complementary_data_validated

    async def validate_enumerate_params(self) -> bool:
        await self._validate_nationality()
        await self._validate_country_acronym()
        await self._validate_marital_status()
        return True

    async def _validate_nationality(self) -> bool:
        spouse = self.complementary_data.get("spouse")
        if not spouse:
            return True
        nationality_code = spouse.get("nationality")
        result = await EnumerateRepository.get_nationality(code=nationality_code)
        if not result:
            raise InvalidNationality
        return True

    async def _validate_country_acronym(self) -> bool:
        foreign_account_tax = self.complementary_data.get("foreign_account_tax")
        if not foreign_account_tax:
            return True
        for tax_residence in foreign_account_tax:
            country_acronym = tax_residence.get("country")
            result = await EnumerateRepository.get_country(country_acronym=country_acronym)
            if not result:
                raise InvalidCountryAcronym
        return True

    async def _validate_marital_status(self) -> bool:
        code = self.complementary_data.get("marital_status")
        result = await EnumerateRepository.get_marital_status(code=code)
        if not result:
            raise InvalidMaritalStatus
        return True
