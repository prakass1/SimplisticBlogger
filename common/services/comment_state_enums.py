import enum

class States(enum.Enum):
    UNDER_MODERATION = 1
    APPROVED = 2
    REJECTED = 3