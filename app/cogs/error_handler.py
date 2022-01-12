from pincer import Client

from app.exceptions import (
    DrinkAlreadyExists,
    DrinkNotFound,
    BotError,
    MemberNotFound,
    MemberAlreadyExists,
    EmployeeNotFound,
    EmployeeFound
)


class ErrorHandler:
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @Client.event
    async def on_command_error(self, error: Exception):
        if not isinstance(error, BotError):
            return

        if isinstance(error, DrinkNotFound):
            return f"La boisson {error.drink_name} n' existe pas !"

        if isinstance(error, DrinkAlreadyExists):
            return f"La boisson {error.drink_name} est déjà enregistrée !"

        if isinstance(error, MemberAlreadyExists):
            return f"Le membre `{error.member_name}` est déjà enregistrée dans `{error.member_type}`"

        if isinstance(error, MemberNotFound):
            return f"Le membre `{error.member_name}` n'est pas dans `{error.member_type}`"

        if isinstance(error, EmployeeNotFound):
            return "Vous n' êtes pas en train de travailler"

        if isinstance(error, EmployeeFound):
            return "Vous êtes déjà dans la liste des employées actifs."


setup = ErrorHandler
