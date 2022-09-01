# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_COMPLEMENTARY_DATA = 6

    def __repr__(self):
        return self.value


class UserOnboardingStep(StrEnum):
    COMPLEMENTARY_DATA = "complementary_data"


class UserOrigins(StrEnum):
    LIGA = "LIGA"


class BureauStatus(StrEnum):
    APPROVED = "approved"
    DOCUMENT = "document"
    REFUSED = "refused"


