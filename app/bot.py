from typing import Optional

import dotenv
from discord import Guild
from discord.ext import commands

GUILD_ID = 888527538710777876


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix='/')
        self.guild: Optional[Guild] = None

        self.remove_command('help')
        self.load_extension('app.cogs.drinks')
        self.load_extension('app.cogs.utils')

    async def on_ready(self) -> None:
        self.guild = self.get_guild(GUILD_ID)

    def run(self):
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))
