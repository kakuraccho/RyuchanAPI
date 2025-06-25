import discord
from discord import app_commands
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_TOKEN = os.getenv('SUPABASE_TOKEN')

supabase = create_client(SUPABASE_URL, SUPABASE_TOKEN)

class MyBot(discort.Client):
    def __init__(self):
        intents = discord.Intents,default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_states = {}
    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.tree.command(name="submit", description="名言(英文)")
async def submit(interaction: discord.Interaction):
    await interaction.response.send_message("名言(英文)を入力してください")
    bot.user_states[interaction.user.id] = "awaiting_input"

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if bot.user_states.get(message.author.id) == "awaiting_input":
        supabase.table("meigen").insert({"meigen_eng": message.content}).execute()
        await message.channel.send("名言を保存しました")
        bot.user_states[message.author.id] = None
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"Logge in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)