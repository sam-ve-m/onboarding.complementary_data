from ..repositories.oracle.repository import SinacorRepository
from ..domain.exceptions import InvalidNationality, InvalidMaritalStatus, InvalidCountryAcronym


class EnumerateService:
    def __init__(self, complementary_data_validated: dict):
        self.complementary_data = complementary_data_validated

    async def validate_enumerate_params(self) -> bool:
        await self._validate_nationality()
        await self._validate_country_acronym()
        await self._validate_marital_status()
        return True

    async def _validate_nationality(self):
        spouse = self.complementary_data.get("spouse")
        if not spouse:
            return True
        nationality_code = spouse.get("nationality")
        result = await SinacorRepository.get_nationality(code=nationality_code)
        if not result:
            raise InvalidNationality
        return True

    async def _validate_country_acronym(self):
        foreign_account_tax = self.complementary_data.get("foreign_account_tax")
        if not foreign_account_tax:
            return True
        country_acronym = foreign_account_tax.get("country")
        result = await SinacorRepository.get_country(country_acronym=country_acronym)
        if not result:
            raise InvalidCountryAcronym
        return True

    async def _validate_marital_status(self):
        code = self.complementary_data.get("marital_status")
        result = await SinacorRepository.get_marital_status(code=code)
        if not result:
            raise InvalidMaritalStatus
        return True
