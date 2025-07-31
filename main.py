import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import logging

class Client(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                extension = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    print(f"Loaded extension {extension}")
                except Exception as e:
                    print(f"Failed to load extension {extension}: {e}")

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} to global commands")
        except Exception as e:
            print(f"Error")

    async def on_ready(self):
        print(f"Bot connected as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix='/', intents=intents, allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
  allowed_installs=discord.app_commands.AppInstallationType(guild=False, user=True ))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

if __name__ == "__main__":
    try:
        client.run(token, log_handler=handler, log_level=logging.DEBUG)
    except KeyboardInterrupt:
        print("Bot stopped manually")



