# Jormungandr - Onboarding
from tests.src.services.complementary_data.stubs import stub_comp_data_model_mandatory

# Third party
import pytest


@pytest.mark.asyncio
async def test_when_have_spouse_then_get_correct_spouse_values():
    user_template = await stub_comp_data_model_mandatory.get_user_update_template()

    assert isinstance(user_template, dict)
    assert user_template.get("marital").get("spouse") is None
