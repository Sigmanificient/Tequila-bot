from typing import TYPE_CHECKING, NoReturn

from discord.ext import commands
from discord.ext.commands import Context, CommandError

from exceptions import DrinkAlreadyExists, DrinkNotFound


class DrinksCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="create",
        description="Créer une nouvelle boisson",
    )
    async def create_command(self, ctx: Context, drink) -> None:
        await self.client.drink_list.create(drink)
        await ctx.send("Boisson ajouté!")

    @commands.command(
        name="add",
        description="Incrémente le compteur d' une boisson"
    )
    async def add_command(self, ctx: Context, drink, n=1) -> None:
        await self.client.drink_list.add(drink, n)
        await ctx.send("Ajouté!")

    @commands.command(
        name="delete",
        description="Retire un boisson de la liste"
    )
    async def delete_command(self, ctx: Context, drink) -> None:
        await self.client.drink_list.delete(drink)
        await ctx.send("Supprimé!")

    @commands.command(
        name="remove",
        description="Décrémente le compteur d' une boisson !"
    )
    async def remove_command(self, ctx: Context, drink, n=1):
        await self.client.drink_list.remove(drink, n)
        await ctx.send("Retiré!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exc: CommandError):
        if isinstance(exc, commands.errors.CommandInvokeError):
            if isinstance(exc.original, DrinkNotFound):
                await ctx.send("cette boisson n' existe pas !")

            if isinstance(exc.original, DrinkAlreadyExists):
                await ctx.send("La boisson est déjà enregistrée !")

        raise exc


def setup(client) -> NoReturn:
    client.add_cog(DrinksCog(client))
