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

supabase = create_client(SUPABASE_URL, SUPABASE_TOKEN)

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_states = {}
    
    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.tree.command(name="meigenSub")
async def submit(interaction: discord.Interaction):
    await interaction.response.send_message("名言(英文)を入力してください")

    def check(m):
        return m.author.id == interaction.user.id and m.channle == interaction.channel
    
    try:
        message = await bot.wait_for("message", check=check, timeout=60.0)
        supabase.table("meigen").insert({"meinge_eng": message.content}).execute()
        await interaction.followup.send("名言を保存しました")
    except asyncio.TimeoutError:
        await interaction.followup.send("時間切れです。もういちど送信してください")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)