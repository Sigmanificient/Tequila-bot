from typing import NoReturn, Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, CommandError

from app.classes.drink_list import DrinkList
from app.exceptions import DrinkAlreadyExists, DrinkNotFound
from app.utils import SALARIED_ROLE_ID, PDG_ROLE_ID

CHANNEL_ID = 888531559861321738
MESSAGE_ID = 888535656542928906


class DrinksCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.name = 'Gestion Boisson'
        self.client = client
        self.channel: Optional[TextChannel] = None
        self.drink_list: Optional[DrinkList] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.drink_list = DrinkList(
            await self.channel.fetch_message(MESSAGE_ID)
        )

    @commands.command(
        name="create",
        description="Créer une nouvelle boisson",
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def create_command(self, ctx: Context, drink) -> None:
        await ctx.message.delete()
        await self.drink_list.create(drink)
        await ctx.send(
            f"Boisson ajouté!\n"
            f">>> {self.drink_list.flatten()}",
            delete_after=3
        )

    @commands.command(
        name="add",
        description="Incrémente le compteur d' une boisson"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def add_command(self, ctx: Context, drink, n=1) -> None:
        await ctx.message.delete()
        await self.drink_list.add(drink, n)
        await ctx.send(
            f"`{drink}`x`{n}` Ajouté!\n"
            f">>> {self.drink_list.flatten()}",
            delete_after=3
        )

    @commands.command(
        name="delete",
        description="Retire un boisson de la liste"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def delete_command(self, ctx: Context, drink) -> None:
        await ctx.message.delete()
        await self.drink_list.delete(drink)
        await ctx.send(
            f"`{drink}` Supprimé!\n"
            f">>> {self.drink_list.flatten()}",
            delete_after=3
        )

    @commands.command(
        name="remove",
        description="Décrémente le compteur d' une boisson"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def remove_command(self, ctx: Context, drink, n=1):
        await ctx.message.delete()
        await self.drink_list.remove(drink, n)
        await ctx.send(
            f"`{drink}` `x`{n} Retiré!\n"
            f">>> {self.drink_list.flatten()}",
            delete_after=3
        )

    @commands.command(
        name="desc-1",
        description="Met à jour la description de la liste de boissons."
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def set_drink_list_description(self, ctx, *, message):
        await ctx.message.delete()

        with open(
            "assets/drinklist_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await ctx.send(
            f"Description mise à jour\n>>> {message}", delete_after=5
        )

        await self.drink_list.update()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exc: CommandError):
        if not isinstance(exc, commands.errors.CommandInvokeError):
            return

        if isinstance(exc.original, DrinkNotFound):
            await ctx.send(
                f"La boisson {exc.original.drink_name} n' existe pas !"
            )

        if isinstance(exc.original, DrinkAlreadyExists):
            await ctx.send(
                f"La boisson {exc.original.drink_name} est déjà enregistrée !"
            )


setup = DrinksCog
