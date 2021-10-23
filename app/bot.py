from typing import Optional, NoReturn, Tuple

import dotenv
from discord import Guild, Activity, ActivityType, Intents
from discord.ext import commands

GUILD_ID: int = 888527538710777876
LOADED_EXTENSIONS: Tuple[str, ...] = (
    'drinks', 'members', 'utils', 'workers', 'tickets'
)


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix='/', intents=Intents.all())
        self.guild: Optional[Guild] = None

        self.remove_command('help')

        for ext in LOADED_EXTENSIONS:
            self.load_extension(f'app.cogs.{ext}')

    async def on_ready(self) -> None:
        self.guild = self.get_guild(GUILD_ID)
        print(self.user, 'is ready')

        await self.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{self.command_prefix}help"
            )
        )

    def run(self) -> NoReturn:
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))
