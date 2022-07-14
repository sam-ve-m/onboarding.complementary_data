from typing import List


class TaxResidenceModel:
    def __init__(self, country, tax_number):
        self.country = country
        self.tax_number = tax_number


class SpouseModel:
    def __init__(self, name, nationality, cpf):
        self.name = name
        self.nationality = nationality
        self.cpf = cpf

    def to_dict(self):
        spouse = {
                "name": self.name,
                "nationality": self.nationality,
                "cpf": self.cpf
        }
        return spouse


class ComplementaryDataModel:
    def __init__(self, complementary_data_validated, unique_id):
        self.unique_id = unique_id
        self.complementary_data = complementary_data_validated
        self.spouse = self._create_spouse_composition()
        self.foreign_account_tax = self._create_foreign_account_tax_composition()
        self.marital_status = complementary_data_validated.get("marital_status")

    def _create_spouse_composition(self) -> SpouseModel:
        spouse = self.complementary_data.get("spouse", None)
        if not spouse:
            return spouse
        name = spouse.get("name")
        nationality = spouse.get("nationality")
        cpf = spouse.get("cpf")
        spouse_model = SpouseModel(name=name, nationality=nationality, cpf=cpf)
        return spouse_model

    def _create_foreign_account_tax_composition(self) -> List[TaxResidenceModel]:
        foreign_account_tax = self.complementary_data.get("foreign_account_tax", None)
        if not foreign_account_tax:
            return foreign_account_tax
        tax_residence_list = [
            TaxResidenceModel(country=tax_residence.get("country"), tax_number=tax_residence.get("tax_number"))
            for tax_residence in foreign_account_tax
        ]
        return tax_residence_list

    async def get_user_update_template(self) -> dict:
        spouse = self.spouse.to_dict() if self.spouse is not None else None
        return {
            "marital": {
                "status": self.marital_status,
                "spouse": spouse,
            }
        }

    async def get_audit_template(self) -> dict:
        spouse = self.spouse.to_dict() if self.spouse is not None else None
        template = {
            "unique_id": self.unique_id,
            "marital": {
                "status": self.marital_status,
                "spouse": spouse
            }
        }
        return template
