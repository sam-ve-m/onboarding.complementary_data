# Jormungandr - Onboarding
from func.src.domain.complementary_data.model import ComplementaryDataModel
from func.src.domain.validators.validator import ComplementaryData
from func.src.domain.models.device_info import DeviceInfo


class UserUpdated:
    def __init__(self, matched_count=None):
        self.matched_count = matched_count


stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {"identifier_document": {"cpf": "123456789"}}
stub_user_same_cpf = {"identifier_document": {"cpf": "03895134074"}}
stub_raw_comp_data_with_optionals = {
    "marital_status": 1,
    "spouse": {"name": "fulano ad", "nationality": 5, "cpf": "038.951.340-74"},
    "foreign_account_tax": [
        {"country": "BRA", "tax_number": "testeteste"},
        {"country": "EUA", "tax_number": "teste2teste2"},
    ],
}

stub_raw_comp_data_only_mandatory = {
    "marital_status": 1,
    "spouse": None,
    "foreign_account_tax": None,
}
stub_user_not_updated = UserUpdated(matched_count=0)
stub_user_updated = UserUpdated(matched_count=1)
stub_comp_data_only_mandatory_validated = ComplementaryData(
    **stub_raw_comp_data_only_mandatory
)
stub_comp_data_with_optionals_validated = ComplementaryData(
    **stub_raw_comp_data_with_optionals
)
stub_device_info = DeviceInfo({"precision": 1}, "")
stub_comp_data_model = ComplementaryDataModel(
    payload_validated=stub_comp_data_with_optionals_validated,
    unique_id=stub_unique_id,
    device_info=stub_device_info,
)
stub_comp_data_model_mandatory = ComplementaryDataModel(
    payload_validated=stub_comp_data_only_mandatory_validated,
    unique_id=stub_unique_id,
    device_info=stub_device_info,
)
