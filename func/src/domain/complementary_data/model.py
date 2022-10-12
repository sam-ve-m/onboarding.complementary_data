# Jormungandr - Onboarding
from ..enums.types import UserOrigins
from ..validators.validator import ComplementaryData

# Standards
from typing import Union


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
    def __init__(self, payload_validated: ComplementaryData, unique_id: str):
        self.unique_id = unique_id
        self.complementary_data = payload_validated
        self.spouse = self._create_spouse_composition()
        self.marital_status = payload_validated.marital_status

    def _create_spouse_composition(self) -> Union[SpouseModel, None]:
        spouse = self.complementary_data.spouse
        if not spouse:
            return spouse
        name = spouse.name
        nationality = spouse.nationality
        cpf = spouse.cpf
        spouse_model = SpouseModel(name=name, nationality=nationality, cpf=cpf)
        return spouse_model

    async def get_user_update_template(self) -> dict:
        spouse = self.spouse.to_dict() if bool(self.spouse) else None
        template = {
            "marital": {
                "status": self.marital_status,
                "spouse": spouse,
            },
            "origin": UserOrigins.LIGA.value,
        }
        return template

    async def get_audit_template(self) -> dict:
        spouse = self.spouse.to_dict() if bool(self.spouse) else None
        template = {
            "unique_id": self.unique_id,
            "marital": {"status": self.marital_status, "spouse": spouse},
        }
        return template
