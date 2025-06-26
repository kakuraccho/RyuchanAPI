import discord
from discord import app_commands
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_TOKEN = os.getenv('SUPABASE_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

supabase = create_client(SUPABASE_URL, SUPABASE_TOKEN)
GUILD = discord.Object(id=GUILD_ID)

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.clear_commands(guild=GUILD)
        await self.tree.sync(guild=GUILD)

bot = MyBot()

@bot.tree.command(name="meigen", description="名言(英文)", guild=GUILD)
async def submit(interaction: discord.Interaction):
    await interaction.response.send_message("名言(英文)を入力してください")

    try:
        message = await bot.wait_for("message", timeout=60.0)
        supabase.table("meigen").insert({"meigen_eng": message.content}).execute()
        await interaction.followup.send("名言を保存しました")
    except asyncio.TimeoutError:
        await interaction.followup.send("時間切れです。もういちど送信してください")

# 動作確認コマンド
@bot.tree.command(name="ping", description="Ping Pong", guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)