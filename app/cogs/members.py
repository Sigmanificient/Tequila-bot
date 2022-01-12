from typing import Optional

from pincer import Client, command
from pincer.objects import TextChannel, InteractionFlags

from app.bot import Bot
from app.classes.members_list import MemberList
from app.exceptions import MemberAlreadyExists, MemberNotFound, BotError

CHANNEL_ID: int = 888563799701991435
MESSAGE_ID: int = 888770216480366632


class MembersCog:
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Gestion Members'
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None
        self.manager = None

    @Client.event
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.manager = MemberList(
            await self.channel.fetch_message(MESSAGE_ID),
        )

    @command(
        name='addpeople',
        description="Ajoute une personne dans la liste des adhérents"
    )
    async def add_people_command(self, person_name: str):
        await self.manager.add(person_name, 'people')
        return (
            'Ajouté!',
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='addcomp',
        description="Ajoute une entreprise dans la liste des adhérents"
    )
    async def add_company_command(self, company_name: str):
        await self.manager.add(company_name, 'company')
        return (
            'Ajouté!',
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='removepeople',
        description="Retire la personne donnée de la liste des adhérents"
    )
    async def remove_people_command(self, company_name: str):
        await self.manager.remove(company_name, 'people')
        return (
            'Retiré!',
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='removecomp',
        description="Retire l'entreprise donnée de la liste des adhérents"
    )
    async def remove_company_command(self, company_name: str):
        await self.manager.remove(company_name, 'company')
        return (
            'Retiré!',
            InteractionFlags.EPHEMERAL
        )

    @command(
        name="desc-2",
        description="Met à jour la description de la liste des adherents."
    )
    async def set_drink_list_description(self, *, message: str):
        with open(
            "assets/members_description.txt",
            'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await self.manager.update()

        return (
            f"Description mise à jour\n>>> {message}",
            InteractionFlags.EPHEMERAL
        )

    @Client.event
    async def on_command_error(self, exc: Exception):
        if not isinstance(exc, BotError):
            return

        if isinstance(exc, MemberAlreadyExists):
            return (
                f"Le membre `{exc.member_name}`"
                f"est déjà enregistrée dans `{exc.original.member_type}`"
            )

        if isinstance(exc.original, MemberNotFound):
            return (
                f"Le membre `{exc.original.member_name}`"
                f"n'est pas dans `{exc.original.member_type}`"
            )


setup = MembersCog
