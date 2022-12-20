from typing import Union

from ..models.device_info import DeviceInfo
from ..validators.validator import ComplementaryData


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
    def __init__(
        self,
        payload_validated: ComplementaryData,
        unique_id: str,
        device_info: DeviceInfo,
    ):
        self.unique_id = unique_id
        self.complementary_data = payload_validated
        self.spouse = self._create_spouse_composition()
        self.marital_status = payload_validated.marital_status
        self.device_info = device_info

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
        spouse = self.spouse.to_dict() if bool(self.spouse) else {}
        template = {
            "marital": {
                "status": self.marital_status,
                "spouse": spouse,
            },
        }
        return template

    async def get_audit_template(self) -> dict:
        spouse = self.spouse.to_dict() if bool(self.spouse) else None
        template = {
            "unique_id": self.unique_id,
            "marital": {"status": self.marital_status, "spouse": spouse},
            "device_info": self.device_info.device_info,
            "device_id": self.device_info.device_id,
        }
        return template
