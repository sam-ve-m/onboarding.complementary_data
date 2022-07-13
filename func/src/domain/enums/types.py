from enum import IntEnum


class QueueTypes(IntEnum):
    USER_COMPLEMENTARY_DATA = 6

    def __repr__(self):
        return self.value
