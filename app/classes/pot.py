import discord

from app.classes.abc.message_manager import MessageManager
from app.utils import get_int


class Pot(MessageManager):

    def __init__(self, message):
        self.pot_message = message
        self.pot = parse_from_message(message.embeds[0].description)

    async def update(self):
        drink_list_embed = discord.Embed(
            title="Cagnotte",
            description=(
                    get_embed_description()
                    + f'\n\n**Total:** `${self.pot:,}`'
            )
        )

        await self.pot_message.edit(
            content='',
            embed=drink_list_embed
        )

    async def add(self, amount):
        self.pot += amount
        await self.update()

    async def correct(self, amount):
        self.pot -= amount
        await self.update()

    async def remove(self, amount):
        self.pot -= amount
        await self.update()


def get_embed_description() -> str:
    with open('assets/pot_description.txt', encoding='utf-8') as f:
        return f.read()


def parse_from_message(content):
    return get_int(content.splitlines()[-1].split('$')[1])
