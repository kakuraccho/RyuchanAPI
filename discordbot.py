# 外部ライブラリのインポート
import discord
from discord import app_commands
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

# 内部ライブラリのインポート
import bot_functions
from config import GUILD_ID, DISCORD_BOT_TOKEN
from bot_functions import MyBot, MeigenModal

# ボット初期化
bot = MyBot(GUILD_ID)

# /meigen
@bot.tree.command(name="meigen", description="名言(英文)", guild=bot.guild)
async def meigen(interaction: discord.Interaction):
    try:
        modal = MeigenModal()
        await interaction.response.send_modal(modal)
    except discord.InteractionResponded:
        await interaction.followup.send("インタラクションは既に処理済みです", ephemeral=True)
    except discord.NotFound:
        print("インタラクションがタイムアウトしました")
    except Exception as e:
        print(f"/meigenコマンドエラー: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message("エラーが発生しました", ephemeral=True)

# /ping
@bot.tree.command(name="ping", description="Ping Pong", guild=bot.guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# エラーハンドラーを追加
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandInvokeError):
        print(f"コマンドエラー: {error}")

        # まだ応答していない場合
        if not interaction.response.is_done():
            try:
                await interaction.response.send_message("コマンドの実行中にエラーが発生しました", ephemeral=True)
            except:
                try:
                    await interaction.followup.send("コマンドの実行中にエラーが発生しました", ephemeral=True)
                except:
                    pass

# メイン実行
if __name__ == "__main__":
    
    if not DISCORD_BOT_TOKEN:
        print("トークンエラー: DISCORD_BOT_TOKENが設定されていません")
        exit(1)

    try:
        print("ボットを起動中...")
        bot.run(DISCORD_BOT_TOKEN)
    except discord.LoginFailure:
        print("ログインエラー: トークンが無効です")
    except Exception as e:
        print(f"ボット起動エラー: {e}")