# ---外部ライブラリのインポート---
import discord
from discord import app_commands
import traceback

# ---内部ライブラリのインポート---
from config import supabase

# ---ボットクラス---
class MyBot(discord.Client):
    def __init__(self, guild_id):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild = discord.Object(id=guild_id)

    async def setup_hook(self):
        """コマンド同期"""
        try:
            synced = await self.tree.sync(guild=self.guild)
            print(f"{len(synced)}個のコマンドを同期しました")
        
        except Exception as e:
            print(f"コマンド同期エラー: {e}")

# ---モーダルクラス---
class MeigenModal(discord.ui.Modal, title='名言(原文)'):
    def __init__(self):
        super().__init__()

    text_input_english = discord.ui.TextInput(
        label='名言(原文)を入力してください',
        style=discord.TextStyle.paragraph,
        placeholder='ここに入力...',
        required=True,
        max_length=4000
    )

    text_input_japanese = discord.ui.TextInput(
        label='名言(意味)を入力してください',
        style=discord.TextStyle.paragraph,
        placeholder='ここに入力...',
        required=True,
        max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        english_text = self.text_input_english.value
        japanese_text = self.text_input_japanese.value

        success, error_message = await save_meigen_to_db(
            english_text,
            japanese_text,
            interaction.user.display_name,
            interaction.guild_id)
        
        if success:
            await interaction.response.send_message(
                f"名言が保存されました:\n```{english_text,english_text}```",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )

# ---/meigen---
async def save_meigen_to_db(text_eng, text_jpn, username, guild_id):
    try:
        result = supabase.table('meigen').insert({
            'text_eng': text_eng,
            'text_jpn': text_jpn,
            'username': username,
            'guild_id': str(guild_id)
        }).execute()
        return True, None
    
    except Exception as e:
        print("--- データベース保存エラー（トレースバック開始）---")
        traceback.print_exc()
        print("--- データベース保存エラー（トレースバック終了）---")
        #print(f"データベース保存エラー: {e}")
        return False, "保存中にエラーが発生しました"