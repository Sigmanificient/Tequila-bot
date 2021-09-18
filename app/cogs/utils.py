import discord
from typing import NoReturn, Optional

from discord.ext import commands
from discord.ext.commands import Context


class DrinksCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.client = client

    @commands.command(
        name="help",
        description="La commande d'aide",
    )
    async def help_command(self, ctx: Context) -> None:
        print(self.client)
        await ctx.send(
            '\n'.join(
                f'- `{cmd.name}`: {cmd.description}'
                for cmd in self.client.all_commands.values()
            )
        )


def setup(client) -> NoReturn:
    client.add_cog(DrinksCog(client))
