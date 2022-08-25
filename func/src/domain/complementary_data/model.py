# Jormungandr - Onboarding
from ..validators.validator import ComplementaryData

# Standards
from typing import List, Union


class TaxResidenceModel:
    def __init__(self, country, tax_number):
        self.country = country
        self.tax_number = tax_number


class SpouseModel:
    def __init__(self, name, nationality, cpf):
        self.name = name
        self.nationality = nationality
        self.cpf = cpf

    def to_dict(self) -> dict:
        spouse = {"name": self.name, "nationality": self.nationality, "cpf": self.cpf}
        return spouse


class ComplementaryDataModel:
    def __init__(self, complementary_data_validated: ComplementaryData, unique_id: str):
        self.unique_id = unique_id
        self.complementary_data = complementary_data_validated
        self.spouse = self._create_spouse_composition()
        self.foreign_account_tax = self._create_foreign_account_tax_composition()
        self.marital_status = complementary_data_validated.marital_status

    def _create_spouse_composition(self) -> Union[SpouseModel, None]:
        spouse = self.complementary_data.spouse
        if not spouse:
            return spouse
        name = spouse.name
        nationality = spouse.nationality
        cpf = spouse.cpf
        spouse_model = SpouseModel(name=name, nationality=nationality, cpf=cpf)
        return spouse_model

    def _create_foreign_account_tax_composition(
        self,
    ) -> Union[List[TaxResidenceModel], None]:
        if foreign_account_tax := self.complementary_data.foreign_account_tax:
            tax_residence_list = [
                TaxResidenceModel(
                    country=tax_residence.country,
                    tax_number=tax_residence.tax_number,
                )
                for tax_residence in foreign_account_tax
            ]
            return tax_residence_list
        return foreign_account_tax

    async def get_user_update_template(self) -> dict:
        spouse = self.spouse.to_dict() if bool(self.spouse) else None
        template = {
            "marital": {
                "status": self.marital_status,
                "spouse": spouse,
            }
        }
        return template

    async def get_audit_template(self) -> dict:
        spouse = self.spouse.to_dict() if bool(self.spouse) else None
        template = {
            "unique_id": self.unique_id,
            "marital": {"status": self.marital_status, "spouse": spouse},
        }
        return template
