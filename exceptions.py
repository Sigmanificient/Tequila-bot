class DrinkError(Exception):

    def __init__(self, drink_name):
        self.drink_name = drink_name


class DrinkAlreadyExists(DrinkError):
    pass


class DrinkNotFound(DrinkError):
    pass
