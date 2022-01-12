from typing import Optional

from pincer import Client
from pincer.objects import TextChannel

from app.bot import Bot

CHANNEL_ID = 900370744263966821
ROLE_ID = 888527962935296091


class WelcomeRole:
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.client: Bot = client
        self.channel: Optional[TextChannel] = None

    @Client.event
    async def on_ready(self):
        self.channel = self.client.guild.get_channel(CHANNEL_ID)

    @Client.event
    async def on_member_update(self, before, after):
        diff_roles = [
            role.id for role in after.roles if role not in before.roles
        ]

        if ROLE_ID in diff_roles:
            await self.channel.send(f"{after.mention}")


setup = WelcomeRole
