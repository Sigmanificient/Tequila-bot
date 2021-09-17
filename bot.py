import discord
import dotenv
from discord import Guild, TextChannel, Message
from discord.ext import commands
from typing import Optional

GUILD_ID = 888527538710777876
CHANNEL_ID = 888531559861321738
MESSAGE_ID = 888535656542928906


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(command_prefix='/')
        self.guild: Optional[Guild] = None
        self.channel: Optional[TextChannel] = None
        self.message: Optional[Message] = None

    async def on_ready(self) -> None:
        self.guild: Guild = self.get_guild(GUILD_ID)
        self.channel: TextChannel = self.guild.get_channel(CHANNEL_ID)
        self.message: Message = await self.channel.fetch_message(MESSAGE_ID)

    def run(self):
        super().run(dotenv.dotenv_values('.env').get('TOKEN'))


if __name__ == '__main__':
    Bot().run()
