class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique id,"
        " jwt not decoded successfully"
    )


class ErrorOnSendAuditLog(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error when trying to send log audit on "
        "Persephone"
    )


class ErrorOnUpdateUser(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error on trying to update user in mongo_db::"
        "User not exists, or unique_id invalid"
    )


class InvalidNationality(ValueError):
    msg = "Jormungandr-Onboarding::_validate_nationality::Nationality not exists"
    pass


class InvalidCountryAcronym(ValueError):
    msg = "Jormungandr-Onboarding::_validate_country_acronym::Country not exists"
    pass


class InvalidMaritalStatus(ValueError):
    msg = "Jormungandr-Onboarding::_validate_marital_status::Marital not exists"
    pass


class InvalidSpouseCpf(Exception):
    msg = "Jormungandr-Onboarding::_validate_marital_status::Spouse's CPF must not e the same"


class InternalServerError(Exception):
    msg = "Jormungandr-Onboarding::OracleBaseRepository::Oracle Internal Server Error"


class UserNotFound(Exception):
    msg = "Jormungandr-Onboarding::_get_user::Not exists an user with this unique_id"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::get_user_current_step::Error when trying to get onboarding steps br"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User is in the {} step"


class InvalidOnboardingAntiFraud(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User rejected by anti fraud"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
