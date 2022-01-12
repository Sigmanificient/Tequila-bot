import asyncio
from time import time
from typing import Optional

from discord import TextChannel, User
from discord.ext import commands
from discord.ext.commands import Context, CommandError
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


class WorkerCog(commands.Cog):
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

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

        self.manager = WorkList(
            await self.channel.fetch_message(MESSAGE_ID),
        )

        await self.manager.update()

    @commands.command(
        name='co',
        description=(
                "Démarre le mode et travail pour garder le temps "
                "et calculer le salaire"
        )
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def connect_command(self, ctx: Context):
        await ctx.message.delete()
        await self.manager.add(ctx.author.id)
        await ctx.send("> Mise au travail...", delete_after=3)

    @commands.command(
        name='add15m',
        description="Ajoute 15m de salaire à la personne mentionnée"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def add_15m_command(self, ctx: Context, user: User = None, amount=1):
        await ctx.message.delete()

        if user is None:
            user = ctx.author

        if user.id not in self.manager.payees:
            self.manager.payees[user.id] = 0

        self.manager.payees[user.id] += (self.manager.paye_amount * amount)

        if self.manager.payees[user.id] == 0:
            self.manager.payees.pop(user.id)

        await self.manager.update()
        await ctx.send("> Ajouté", delete_after=3)

    @commands.command(
        name='remove15m',
        description="Retire 15m de salaire à la personne mentionnée"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def remove_15m_command(
            self, ctx: Context, user: User = None, amount=1
    ):
        await ctx.message.delete()

        if user is None:
            user = ctx.author

        if user.id not in self.manager.payees:
            self.manager.payees[user.id] = 0

        self.manager.payees[user.id] -= (self.manager.paye_amount * amount)

        if self.manager.payees[user.id] == 0:
            self.manager.payees.pop(user.id)

        await self.manager.update()
        await ctx.send("> Retiré", delete_after=3)

    @commands.command(
        name='deco',
        description="Arrête le mode travail."
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def disconnect(self, ctx: Context):
        await ctx.message.delete()
        await self.manager.remove(ctx.author.id)
        await ctx.send('> Arrêt', delete_after=3)

    @commands.command(
        name='wipe',
        description="Supprime la liste des salaries à payer."
    )
    async def wipe(self, ctx: Context):
        await self.manager.wipe()
        await ctx.send("> Wiped!")

    @commands.command(
        name="desc-3",
        description="Met à jour la description de la liste de travail."
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def set_drink_list_description(self, ctx, *, message):
        await ctx.message.delete()

        with open(
                "assets/worklist_description.txt",
                'w', encoding='utf-8'
        ) as f:
            f.write(message)

        await ctx.send(
            f"Description mise à jour\n>>> {message}", delete_after=5
        )

        await self.manager.update()

    @commands.command(name="pay")
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def set_pay_command(self, ctx: Context, amount: int):
        await ctx.message.delete()

        self.manager.paye_amount = amount
        await self.manager.update()
        await ctx.send(
            f"La paye est maintenant de `${amount:,}`", delete_after=5
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exc: CommandError):
        if not isinstance(exc, commands.errors.CommandInvokeError):
            return

        if isinstance(exc.original, EmployeeNotFound):
            await ctx.send(
                "Vous n' êtes pas en train de travailler"
            )

        if isinstance(exc.original, EmployeeFound):
            await ctx.send("Vous êtes déjà dans la liste des employées actifs.")


setup = WorkerCog
