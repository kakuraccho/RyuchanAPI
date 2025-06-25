import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))  # .env にギルドIDを入れておく

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild = discord.Object(id=GUILD_ID)

    async def setup_hook(self):
        # 起動時にコマンドを一旦全削除して再同期
        await self.tree.clear_commands(guild=self.guild)
        await self.tree.sync(guild=self.guild)

bot = MyBot()

@bot.tree.command(name="meigen", description="名言(英文)", guild=bot.guild)
async def meigen_command(interaction: discord.Interaction):
    await interaction.response.send_message("名言(英文)を入力してください")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)
