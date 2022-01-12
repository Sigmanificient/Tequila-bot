from typing import NoReturn, Optional

from pincer import Client, command
from pincer.objects import InteractionFlags, TextChannel

from app.bot import Bot
from app.classes.pot import Pot
from app.utils import SALARIED_ROLE_ID, PDG_ROLE_ID

CHANNEL_ID: int = 889523568298307594
MESSAGE_ID: int = 890313495030157313


class TicketCog:
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Cagnotte'
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None
        self.pot: Optional[Pot] = None

    @Client.event
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.pot = Pot(
            await self.channel.fetch_message(MESSAGE_ID),
        )

        await self.pot.update()

    @command(
        name="vente",
        description="Ajoute le montant rapporté par la cagnotte"
    )
    async def sell_command(self, amount: int):
        await self.pot.add(amount)
        return (
            "> Ajouté!",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="erreur",
        description="Corrige une erreur sur la cagnotte"
    )
    async def error_remove_command(self, amount: int):
        await self.pot.correct(amount)
        return (
            "> Corrigé",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="achat",
        description="Retire le montant utilisé depuis la cagnotte"
    )
    async def buy_remove_command(self, amount: int):
        await self.pot.remove(amount)
        return (
            "> Retiré",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="desc-4",
        description="Met à jour la description de la cagnotte."
    )
    async def set_drink_list_description(self, message: str):
        with open(
            "assets/pot_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await self.pot.update()
        return (
            f"Description mise à jour\n>>> {message}",
            InteractionFlags.EPHEMERAL
        )


setup = TicketCog
