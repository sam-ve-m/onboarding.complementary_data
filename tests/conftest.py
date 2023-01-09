# Jormungandr - Onboarding
from func.src.services.user_enumerate_data import EnumerateService
from func.src.services.validate_rules import ValidateRulesService
from tests.src.services.complementary_data.stubs import (
    stub_comp_data_only_mandatory_validated,
    stub_comp_data_with_optionals_validated,
    stub_unique_id,
)

# Third party
from pytest import fixture


@fixture(scope="function")
def comp_data_service():
    service = ValidateRulesService(
        unique_id=stub_unique_id,
        payload_validated=stub_comp_data_with_optionals_validated,
        jwt="123",
    )
    return service


@fixture(scope="function")
def comp_data_service_only_mandatory():
    service = ValidateRulesService(
        unique_id=stub_unique_id,
        payload_validated=stub_comp_data_only_mandatory_validated,
        jwt="123",
    )
    return service


@fixture(scope="function")
def enumerate_service():
    service = EnumerateService(
        complementary_data_validated=stub_comp_data_with_optionals_validated
    )
    return service


@fixture(scope="function")
def enumerate_service_only_mandatory():
    service = EnumerateService(
        complementary_data_validated=stub_comp_data_only_mandatory_validated
    )
    return service
