from typing import NoReturn, Optional

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, CommandError

from app.bot import Bot
from app.classes.members_list import MemberList
from app.exceptions import MemberAlreadyExists, MemberNotFound
from app.utils import SALARIED_ROLE_ID, PDG_ROLE_ID

CHANNEL_ID: int = 888563799701991435
MESSAGE_ID: int = 888770216480366632


class MembersCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Gestion Members'
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None
        self.manager = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.manager = MemberList(
            await self.channel.fetch_message(MESSAGE_ID),
        )

    @commands.command(
        name='addpeople',
        description="Ajoute une personne dans la liste des adhérents"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def add_people_command(self, ctx: Context, person_name: str):
        await ctx.message.delete()
        await self.manager.add(person_name, 'people')
        await ctx.send('Ajouté!', delete_after=2)

    @commands.command(
        name='addcomp',
        description="Ajoute une entreprise dans la liste des adhérents"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def add_company_command(self, ctx: Context, company_name: str):
        await ctx.message.delete()
        await self.manager.add(company_name, 'company')
        await ctx.send('Ajouté!', delete_after=2)

    @commands.command(
        name='removepeople',
        description="Retire la personne donnée de la liste des adhérents"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def remove_people_command(self, ctx: Context, company_name: str):
        await ctx.message.delete()
        await self.manager.remove(company_name, 'people')
        await ctx.send('Retiré!', delete_after=2)

    @commands.command(
        name='removecomp',
        description="Retire l'entreprise donnée de la liste des adhérents"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def remove_company_command(self, ctx: Context, company_name: str):
        await ctx.message.delete()
        await self.manager.remove(company_name, 'company')
        await ctx.send('Retiré!', delete_after=2)

    @commands.command(
        name="desc-2",
        description="Met à jour la description de la liste des adherents."
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def set_drink_list_description(self, ctx: Context, *, message: str):
        await ctx.message.delete()

        with open(
            "assets/members_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await ctx.send(
            f"Description mise à jour\n>>> {message}", delete_after=5
        )

        await self.manager.update()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exc: CommandError):
        if not isinstance(exc, commands.errors.CommandInvokeError):
            return

        if isinstance(exc.original, MemberAlreadyExists):
            await ctx.send(
                f"Le membre `{exc.original.member_name}`"
                f"est déjà enregistrée dans `{exc.original.member_type}`"
            )

        if isinstance(exc.original, MemberNotFound):
            await ctx.send(
                f"Le membre `{exc.original.member_name}`"
                f"n'est pas dans `{exc.original.member_type}`"
            )


def setup(client) -> NoReturn:
    client.add_cog(MembersCog(client))
