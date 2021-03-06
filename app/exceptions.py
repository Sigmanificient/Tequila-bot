class BotError(Exception):
    """A custom exception class to wrap bot errors."""
    pass


class DrinkError(BotError):
    """An Base Exception for Drinks Errors."""

    def __init__(self, drink_name: str):
        self.drink_name = drink_name


class DrinkAlreadyExists(DrinkError):
    """Raised when a drink is already in the database."""
    pass


class DrinkNotFound(DrinkError):
    """Raised when a drink isn't found in the database."""
    pass


class MemberError(BotError):
    """An Base Exception for Member Errors."""

    def __init__(self, member_name: str, member_type: str):
        self.member_name = member_name
        self.member_type = member_type


class MemberAlreadyExists(MemberError):
    """Raised when a member with the given name already exists in database."""
    pass


class MemberNotFound(MemberError):
    """Raised when a member with the given isn't found within the database."""
    pass


class EmployeeError(BotError):
    """An Base Exception for Worker Errors."""

    def __init__(self, employee_name: str):
        self.employee_name = employee_name


class EmployeeFound(EmployeeError):
    """Raised when a worker is already working."""
    pass


class EmployeeNotFound(EmployeeError):
    """Raised when a worker is not yet working."""
    pass
