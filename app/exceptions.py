class DrinkError(Exception):

    def __init__(self, drink_name):
        self.drink_name = drink_name


class DrinkAlreadyExists(DrinkError):
    pass


class DrinkNotFound(DrinkError):
    pass


class MemberError(Exception):

    def __init__(self, member_name, member_type):
        self.member_name = member_name
        self.member_type = member_type


class MemberAlreadyExists(MemberError):
    pass


class MemberNotFound(MemberError):
    pass
