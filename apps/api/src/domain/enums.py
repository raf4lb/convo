from enum import Enum


class UserTypes(Enum):
    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    STAFF = "staff"


class ChatStatuses(Enum):
    OPEN = "open"
    PENDING = "pending"
    REPLIED = "replied"
    CLOSED = "closed"
