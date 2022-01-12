import asyncio
from time import time
from typing import Optional

from pincer import Client, command
from pincer.objects import TextChannel, MessageContext, InteractionFlags, User
from pincer.utils import TaskScheduler

from app.bot import Bot
from app.classes.work_list import WorkList
from app.exceptions import EmployeeFound, EmployeeNotFound
from app.tasks.update_salaries import UpdateSalariesTask
from app.utils import QUARTER_HOUR, get_last_q_hour

CHANNEL_ID: int = 888821011989012551
MESSAGE_ID: int = 920438493321248769
SALARIED_ROLE_ID: int = 888527962935296091
PDG_ROLE_ID: int = 888527789794422784


class WorkerCog:
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Travail'
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None
        self.manager: Optional[WorkList] = None

        task = TaskScheduler(self.client)
        await asyncio.sleep((get_last_q_hour() + QUARTER_HOUR) - time())

        update_salaries_cls = UpdateSalariesTask(self.manager)

        self.update_salaries = task.loop(minutes=QUARTER_HOUR)(update_salaries_cls.update_salaries)
        self.update_salaries.start()

    @Client.event
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.manager = WorkList(
            await self.channel.fetch_message(MESSAGE_ID),
        )

        await self.manager.update()

    @command(
        name='co',
        description=(
                "Démarre le mode et travail pour garder le temps "
                "et calculer le salaire"
        )
    )
    async def connect_command(self, ctx: MessageContext):
        await self.manager.add(ctx.author.id)
        return (
            "> Mise au travail...",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='add15m',
        description="Ajoute 15m de salaire à la personne mentionnée"
    )
    async def add_15m_command(self, ctx: MessageContext, user: User = None, amount=1):

        if user is None:
            user = ctx.author

        if user.id not in self.manager.payees:
            self.manager.payees[user.id] = 0

        self.manager.payees[user.id] += (self.manager.paye_amount * amount)

        if self.manager.payees[user.id] == 0:
            self.manager.payees.pop(user.id)

        await self.manager.update()
        await ctx.send("> Ajouté", delete_after=3)

    @command(
        name='remove15m',
        description="Retire 15m de salaire à la personne mentionnée"
    )
    async def remove_15m_command(
            self, ctx: MessageContext, user: User = None, amount=1
    ):
        if user is None:
            user = ctx.author

        if user.id not in self.manager.payees:
            self.manager.payees[user.id] = 0

        self.manager.payees[user.id] -= (self.manager.paye_amount * amount)

        if self.manager.payees[user.id] == 0:
            self.manager.payees.pop(user.id)

        await self.manager.update()
        return (
            "> Retiré",
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='deco',
        description="Arrête le mode travail."
    )
    async def disconnect(self, ctx: MessageContext):
        await self.manager.remove(ctx.author.id)
        return (
            '> Arrêt',
            InteractionFlags.EPHEMERAL
        )

    @command(
        name='wipe',
        description="Supprime la liste des salaries à payer."
    )
    async def wipe(self):
        await self.manager.wipe()
        return "> Wiped!"

    @command(
        name="desc-3",
        description="Met à jour la description de la liste de travail."
    )
    async def set_drink_list_description(self, ctx, message):
        with open(
                "assets/worklist_description.txt",
                'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await self.manager.update()
        return (
            f"Description mise à jour\n>>> {message}",
            InteractionFlags.EPHEMERAL
        )

    @command(name="pay")
    async def set_pay_command(self, amount: int):
        self.manager.paye_amount = amount
        await self.manager.update()

        return (
            f"La paye est maintenant de `${amount:,}`",
            InteractionFlags.EPHEMERAL
        )

setup = WorkerCog
