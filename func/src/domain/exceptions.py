class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Error when trying to send log audit on Persephone"


class ErrorOnUpdateUser(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Error on trying to update user in mongo_db::" \
          "User not exists, or unique_id invalid"


class InvalidNationality(ValueError):
    msg = "Nationality not exists"
    pass


class InvalidCountryAcronym(ValueError):
    msg = "Country not exists"
    pass


class InvalidMaritalStatus(ValueError):
    msg = "Marital not exists"
    pass


class InvalidSpouseCpf(Exception):
    msg = "Spouse's CPF must not e the same"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Not exists an user with this unique_id"
