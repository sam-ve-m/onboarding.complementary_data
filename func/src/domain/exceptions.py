class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Not exists an user with this unique_id"


class TermVersionNotExists(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Not exists an user with this unique_id"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Error when trying to send log audit on Persephone"


class ErrorOnUpdateUser(Exception):
    msg = "Jormungandr-Onboarding::terms_sign::Error on trying to update user in mongo_db::" \
          "User not exists, or unique_id invalid"


class InternalServerError(Exception):
    pass
