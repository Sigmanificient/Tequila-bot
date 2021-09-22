import discord

from app.classes.abc.message_manager import MessageManager
from app.exceptions import EmployeeFound, EmployeeNotFound
from app.utils import get_int, get_last_half_hour


class WorkList(MessageManager):

    def __init__(self, message):
        self.work_list_message = message

        fields = message.embeds[0].fields

        self.paye_amount = 1200

        self.work_list = parse_from_message(
            fields[0].value, 'Aucun employés actifs', ' || '
        )

        self.payees = parse_from_message(
            fields[1].value, 'Pas de salaires enregistré', '$'
        )

    async def update(self):
        drink_list_embed = discord.Embed(
            title="Travail",
            description=get_embed_description()
        ).add_field(
            name="Actifs",
            value='\n'.join(
                f'- <@{employee_name}> || {start_time} ||'
                for employee_name, start_time in self.work_list.items()
            ) or 'Aucun employés actifs'
        ).add_field(
            name="Payes",
            value='\n'.join(
                f'- <@{employee_name}> `${payee:,}`'
                for employee_name, payee in self.payees.items()
            ) or 'Pas de salaires enregistré',
            inline=False
        ).add_field(
            name='Tarif (30min)',
            value=f'> `${self.paye_amount:,}`'
        )

        await self.work_list_message.edit(
            content='',
            embed=drink_list_embed
        )

    async def update_salaries(self):
        for employee_name in list(self.work_list.keys()):
            if self.payees.get(employee_name) is None:
                self.payees[employee_name] = 0

            self.payees[employee_name] += self.paye_amount

        await self.update()

    async def add(self, worker, t=0):
        if worker in self.work_list:
            raise EmployeeFound(worker)

        self.work_list[worker] = t or get_last_half_hour()
        await self.update()

    async def remove(self, worker):
        if worker not in self.work_list:
            raise EmployeeNotFound(worker)

        self.work_list.pop(worker)
        await self.update()

    async def wipe(self):
        self.payees = {}
        await self.update()


def get_embed_description() -> str:
    with open('assets/worklist_description.txt', encoding='utf-8') as f:
        return f.read()


def parse_from_message(content, empty, delim):
    if content == empty:
        return {}

    parsed = {}
    for line in content.splitlines():
        left, right = line.split(delim)
        parsed[get_int(left)] = get_int(right)

    return parsed
