from ..repositories.oracle.repository import SinacorRepository


class EnumerateService:
    def __init__(self, complementary_data_validated):
        self.complementary_data = complementary_data_validated

    @staticmethod
    def validate_params(complementary_data_validated: dict) -> bool:
        code = complementary_data_validated.get("marital_status")
        spouse = complementary_data_validated.get("spouse")
        foreign_account_tax = complementary_data_validated.get("foreign_account_tax")
        if not spouse or not foreign_account_tax:
            raise Exception
        nationality_code = spouse.get("nationality")
        country_acronym = foreign_account_tax.get("country")
        nationality_result = await SinacorRepository.get_nationality(code=nationality_code)
        country_result = await SinacorRepository.get_country(country_acronym=country_acronym)
        marital_result = await SinacorRepository.get_marital_status(code=code)
        if not nationality_result or not country_result or not marital_result:
            raise Exception
        return True

    async def validate_nationality(self):
        spouse = self.complementary_data.get("spouse")
        if not spouse:
            raise Exception
        nationality_code = spouse.get("nationality")
        result = await SinacorRepository.get_nationality(code=nationality_code)
        if not result:
            raise Exception

    async def validate_country_acronym(self):
        foreign_account_tax = self.complementary_data.get("foreign_account_tax")
        if not foreign_account_tax:
            raise Exception
        country_acronym = foreign_account_tax.get("country")
        result = await SinacorRepository.get_country(country_acronym=country_acronym)
        if not result:
            raise Exception
        return True

    async def validate_marital_status(self):
        code = self.complementary_data.get("marital_status")
        result = await SinacorRepository.get_marital_status(code=code)
        if not result:
            raise Exception
        return True
