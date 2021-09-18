from typing import Optional, NoReturn, Tuple

import dotenv
from discord import Guild
from discord.ext import commands

GUILD_ID: int = 888527538710777876
LOADED_EXTENSIONS: Tuple[str, ...] = ('drinks', 'members', 'utils')


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix='/')
        self.guild: Optional[Guild] = None

        self.remove_command('help')

        for ext in LOADED_EXTENSIONS:
            self.load_extension(f'app.cogs.{ext}')

    async def on_ready(self) -> None:
        self.guild = self.get_guild(GUILD_ID)
        print(self.user, 'is ready')

    def run(self) -> NoReturn:
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))
