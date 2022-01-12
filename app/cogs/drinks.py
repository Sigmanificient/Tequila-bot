from typing import Optional

from pincer import Client, command
from pincer.objects import TextChannel, MessageContext, InteractionFlags

from app.classes.drink_list import DrinkList
from app.exceptions import DrinkAlreadyExists, DrinkNotFound, BotError

CHANNEL_ID = 888531559861321738
MESSAGE_ID = 888535656542928906


class DrinksCog:
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.name = 'Gestion Boisson'
        self.client = client
        self.channel: Optional[TextChannel] = None
        self.drink_list: Optional[DrinkList] = None

    @Client.event
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.drink_list = DrinkList(
            await self.channel.fetch_message(MESSAGE_ID)
        )

    @command(
        name="create",
        description="Créer une nouvelle boisson",
    )
    async def create_command(self, drink):
        await self.drink_list.create(drink)
        return (
            f"Boisson ajouté!\n"
            f">>> {self.drink_list.flatten()}",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="add",
        description="Incrémente le compteur d' une boisson"
    )
    async def add_command(self, drink, n=1):
        await self.drink_list.add(drink, n)
        return (
            f"`{drink}`x`{n}` Ajouté!\n"
            f">>> {self.drink_list.flatten()}",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="delete",
        description="Retire un boisson de la liste"
    )
    async def delete_command(self, drink):
        await self.drink_list.delete(drink)
        return (
            f"`{drink}` Supprimé!\n"
            f">>> {self.drink_list.flatten()}",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="remove",
        description="Décrémente le compteur d' une boisson"
    )
    async def remove_command(self, drink, n=1):
        await self.drink_list.remove(drink, n)
        return (
            f"`{drink}` `x`{n} Retiré!\n"
            f">>> {self.drink_list.flatten()}",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="desc-1",
        description="Met à jour la description de la liste de boissons."
    )
    async def set_drink_list_description(self, ctx, *, message):
        await ctx.message.delete()

        with open(
            "assets/drinklist_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await self.drink_list.update()
        return (
            f"Description mise à jour\n>>> {message}",
            InteractionFlags.EPHEMERAL
        )



setup = DrinksCog
