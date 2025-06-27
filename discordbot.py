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

# ---環境変数のチェック---
if not all([DISCORD_BOT_TOKEN, SUPABASE_URL, SUPABASE_TOKEN, GUILD_ID]):
    raise ValueError("環境変数に異常があります")


supabase = create_client(SUPABASE_URL, SUPABASE_TOKEN)
GUILD = discord.Object(id=GUILD_ID)

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        # ---コマンド同期のエラーハンドリング---
        try:
            synced = await self.tree.sync(guild=GUILD)
            print(f"{len(synced)}個のコマンドを同期しました")
        except Exception as e:
            print(f"コマンド同期エラー: {e}")

class MeigenModal(discord.ui.Modal, title='名言(英文)'):
    def __init__(self):
        super().__init__()

    text_input = discord.ui.TextInput(
        label='名言(英文)を入力してください',
        style=discord.TextStyle.paragraph,
        placeholder='ここに入力...',
        required=True,
        max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        english_text = self.text_input.value #入力されたテキストを取得
        
        try:
            # ---supabaseに名言を保存---
            result = supabase.table('meigen').insert({
                'text': english_text,
                'user_id': str(interaction.user.id),
                'username': interaction.user.display_name,
                'guild_id': str(interaction.guild_id)
            }).execute()

            await interaction.response.send_message(
                f"名言が保存されました:\n```{english_text}```",
                ephemeral=True
            )

        except Exception as e:
            print(f"データベースエラー: {e}")
            await interaction.response.send_message(
                "名言の保存に失敗しました。再度お試しください。",
                ephemeral=True
            )


bot = MyBot()

@bot.tree.command(name="meigen", description="名言(英文)", guild=GUILD)
async def meigen(interaction: discord.Interaction):
    modal = MeigenModal()
    
    await interaction.response.send_modal(modal)


# 動作確認コマンド
@bot.tree.command(name="ping", description="Ping Pong", guild=GUILD)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)