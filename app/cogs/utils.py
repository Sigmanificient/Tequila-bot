from app.bot import Bot
from typing import NoReturn, Optional

import discord
import psutil

from discord.ext import commands
from discord.ext.commands import Context, CommandError

SALARIED_ROLE_ID: int = 888527962935296091
PDG_ROLE_ID: int = 888527789794422784


class UtilsCog(commands.Cog):
    """A simple commands cog template."""

    def __init__(self, client: Bot):
        """Link to bot instance."""
        self.name = 'Utilitaire'
        self.client: Bot = client

    @commands.command(
        name='pan',
        description='host stats'
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def panel_info(self, ctx: Context):
        await ctx.message.delete()
        mb: int = 1024 ** 2

        vm = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage('.')

        stats = {
            'ram': (
                100 * (vm.used / vm.total),
                f'{(vm.total / mb) / 1000:,.3f}',
                'Gb'
            ),
            'cpu': (
                cpu_percent,
                f"{cpu_freq.current / 1000:.1f}`/`{cpu_freq.max / 1000:.1f}",
                'Ghz'
            ),
            'disk': (
                100 * (disk.used / disk.total),
                f'{disk.total / mb:,.0f}', 'Mb'
            )
        }

        panel_embed = discord.Embed(
            title="Server Report",
            description="The bot is hosted on a private vps."
        )

        for name, (percent, info, unit) in stats.items():
            panel_embed.add_field(
                name=name.upper(),
                value=f"> `{percent:.3f}` **%**\n- `{info}` **{unit}**"
            )

        await ctx.send(embed=panel_embed)

    @commands.command(
        name="help",
        description="La commande d'aide",
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def help_command(self, ctx: Context):
        await ctx.message.delete()

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

        await ctx.send(embed=help_embed, delete_after=60)

    @commands.command(
        name="purge",
        description="Supprime X messages"
    )
    @commands.has_any_role(SALARIED_ROLE_ID, PDG_ROLE_ID)
    async def purge_command(
            self, ctx: Context, limit: Optional[int] = None
    ) -> None:
        await ctx.channel.purge(limit=limit)
        await ctx.send("> Purgé!", delete_after=5)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exc: CommandError):
        print(exc)

        if isinstance(exc, commands.errors.MissingAnyRole):
            await ctx.send(
                "> Seul les salariés ont le droit d' exécuter cette commande."
            )


def setup(client: Bot) -> NoReturn:
    client.add_cog(UtilsCog(client))
