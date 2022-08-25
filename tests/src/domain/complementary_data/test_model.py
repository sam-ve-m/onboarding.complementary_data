# Jormungandr - Onboarding
from tests.src.services.complementary_data.stubs import (
    stub_comp_data_model_mandatory,
    stub_comp_data_model,
)

# Third party
import pytest


@pytest.mark.asyncio
async def test_when_not_have_spouse_then_return_expected_user_template_values():
    user_template = await stub_comp_data_model_mandatory.get_user_update_template()

    assert isinstance(user_template, dict)
    assert user_template.get("marital").get("spouse") is None


@pytest.mark.asyncio
async def test_when_have_spouse_then_return_expected_user_template_values():
    user_template = await stub_comp_data_model.get_user_update_template()

    assert isinstance(user_template, dict)
    assert user_template.get("marital").get("spouse").get("name") == "fulano"
    assert user_template.get("marital").get("spouse").get("cpf") == "03895134074"
    assert user_template.get("marital").get("spouse").get("nationality") == 5


@pytest.mark.asyncio
async def test_when_not_have_spouse_then_return_expected_audit_template_values():
    user_template = await stub_comp_data_model_mandatory.get_audit_template()

    assert isinstance(user_template, dict)
    assert user_template.get("marital").get("spouse") is None


@pytest.mark.asyncio
async def test_when_have_spouse_then_return_expected_audit_template_values():
    user_template = await stub_comp_data_model.get_user_update_template()

    assert isinstance(user_template, dict)
    assert user_template.get("marital").get("spouse").get("name") == "fulano"
    assert user_template.get("marital").get("spouse").get("cpf") == "03895134074"
    assert user_template.get("marital").get("spouse").get("nationality") == 5


@pytest.mark.asyncio
async def test_when_have_account_tax_then_return_expected_composition():
    tax_residence_list = stub_comp_data_model._create_foreign_account_tax_composition()

    assert bool(tax_residence_list)


@pytest.mark.asyncio
async def test_when_not_have_account_tax_then_return_expected_composition():
    tax_residence_list = (
        stub_comp_data_model_mandatory._create_foreign_account_tax_composition()
    )

    assert not tax_residence_list
