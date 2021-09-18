from typing import NoReturn

import discord
from discord.ext import commands
from discord.ext.commands import Context

SALARIED_ROLE_ID = 888527962935296091
PDG_ROLE_ID = 888527789794422784


class UtilsCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client):
        """Link to bot instance."""
        self.name = 'Utilitaire'
        self.client = client

    @commands.command(
        name="help",
        description="La commande d'aide",
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def help_command(self, ctx: Context) -> None:

        help_embed = discord.Embed(
            description="Aide du TéquilaBot"
        )

        for cog in self.client.cogs.values():
            help_embed.add_field(
                name=f'> {cog.name}',
                value='\n'.join(
                   f'- `{command.name}`: {command.description}'
                   for command in cog.get_commands()
                ), inline=False
            )

        await ctx.send(embed=help_embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, commands.errors.MissingAnyRole):
            await ctx.send(
                "> Seul les salariés ont le droit d' exécuter cette commande."
            )

        else:
            print(exc)


def setup(client) -> NoReturn:
    client.add_cog(UtilsCog(client))
