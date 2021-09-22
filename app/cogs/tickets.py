from typing import NoReturn, Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context

from app.bot import Bot
from app.classes.pot import Pot
from app.utils import SALARIED_ROLE_ID, PDG_ROLE_ID

CHANNEL_ID: int = 889523568298307594
MESSAGE_ID: int = 890313495030157313


class TicketCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Cagnotte'
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None
        self.pot: Optional[Pot] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.pot = Pot(
            await self.channel.fetch_message(MESSAGE_ID),
        )

        await self.pot.update()

    @commands.command(
        name="vente",
        description="Ajoute le montant rapporté par la cagnotte"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def sell_command(self, ctx: Context, amount: int):
        await ctx.message.delete()
        await self.pot.add(amount)
        await ctx.send("> Ajouté!", delete_after=3)

    @commands.command(
        name="erreur",
        description="Corrige une erreur sur la cagnotte"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def error_remove_command(self, ctx: Context, amount: int):
        await ctx.message.delete()
        await self.pot.correct(amount)
        await ctx.send("> Corrigé", delete_after=3)

    @commands.command(
        name="achat",
        description="Retire le montant utilisé depuis la cagnotte"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def buy_remove_command(self, ctx: Context, amount: int):
        await ctx.message.delete()
        await self.pot.remove(amount)
        await ctx.send("> Retiré", delete_after=3)

    @commands.command(
        name="desc-4",
        description="Met à jour la description de la cagnotte."
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def set_drink_list_description(self, ctx: Context, *, message: str):
        await ctx.message.delete()

        with open(
            "assets/pot_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await ctx.send(
            f"Description mise à jour\n>>> {message}", delete_after=5
        )

        await self.pot.update()


def setup(client) -> NoReturn:
    client.add_cog(TicketCog(client))
