# Jormungandr - Onboarding
from func.src.domain.validator import ComplementaryData


class UserUpdated:
    def __init__(self, acknowledged=None):
        self.acknowledged = acknowledged


stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {
    "identifier_document": {
        "cpf": "123456789"
    }
}
stub_user_same_cpf = {
    "identifier_document": {
        "cpf": "03895134074"
    }
}
stub_raw_comp_data_with_optionals = {
    "marital_status": 1,
    "spouse": {
        "name": "fulano",
        "nationality": 5,
        "cpf": "038.951.340-74"
    },
    "foreign_account_tax": [
        {
            "country": "BRA",
            "tax_number": "testeteste"
        },
        {
            "country": "EUA",
            "tax_number": "teste2teste2"
        }
    ]
}

stub_raw_comp_data_only_mandatory = {
    "marital_status": 1,
    "spouse": None,
    "foreign_account_tax": None
}
stub_user_not_updated = UserUpdated(acknowledged=False)
stub_user_updated = UserUpdated(acknowledged=True)
stub_comp_data_only_mandatory_validated = ComplementaryData(**stub_raw_comp_data_only_mandatory).dict()
stub_comp_data_with_optionals_validated = ComplementaryData(**stub_raw_comp_data_with_optionals).dict()
