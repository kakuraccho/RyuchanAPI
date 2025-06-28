# ---外部ライブラリのインポート---
import discord
from discord import app_commands
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

# ---内部ライブラリのインポート---
import bot_functions
from config import GUILD_ID, DISCORD_BOT_TOKEN
from bot_functions import MyBot, MeigenModal

# ボット初期化
bot = MyBot(GUILD_ID)

# /meigen
@bot.tree.command(name="meigen", description="名言(英文)", guild=bot.guild)
async def meigen(interaction: discord.Interaction):
    modal = MeigenModal()
    
    await interaction.response.send_modal(modal)

# /ping
@bot.tree.command(name="ping", description="Ping Pong", guild=bot.guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# メイン実行
if __name__ == "__main__":
    try:
        bot.run(DISCORD_BOT_TOKEN)
        print(f"Logged in as {bot.user}")
    except Exception as e:
        print(f"ボット起動エラー: {e}")