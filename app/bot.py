from typing import Optional, Tuple

import dotenv
from discord import Guild
from pincer import Client

GUILD_ID: int = 888527538710777876
LOADED_EXTENSIONS: Tuple[str, ...] = (
    'drinks', 'members', 'utils', 'workers', 'tickets'
)


class Bot(Client):

    def __init__(self) -> None:
        super().__init__(dotenv.dotenv_values('.env').get('TOKEN'))
        self.guild: Optional[Guild] = None

        for ext in LOADED_EXTENSIONS:
            self.load_cog(f'app.cogs.{ext}')

    async def on_ready(self) -> None:
        self.guild = self.get_guild(GUILD_ID)
        print(self.user, 'is ready')

        # await self.change_presence(
        #    activity=Activity(
        #        type=ActivityType.watching,
        #        name=f"{self.command_prefix}help"
        #    )
        # )
