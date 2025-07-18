# 外部ライブラリのインポート
import discord
from discord import app_commands
import traceback
import asyncio

# 内部ライブラリのインポート
from config import supabase

# ---クラス定義---
# ボットクラス
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

# モーダルクラス
class MeigenModal(discord.ui.Modal, title='名言'):
    def __init__(self):
        super().__init__(timeout=300)

    text_input_english = discord.ui.TextInput(
        label='名言(原文)を入力してください',
        style=discord.TextStyle.paragraph,
        placeholder='ここに入力...',
        required=True,
        max_length=4000,
        min_length=1
    )

    text_input_japanese = discord.ui.TextInput(
        label='名言(意味)を入力してください',
        style=discord.TextStyle.paragraph,
        placeholder='ここに入力...',
        required=True,
        max_length=4000,
        min_length=1
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)

            english_text = self.text_input_english.value
            japanese_text = self.text_input_japanese.value

            success, error_message = await save_meigen_to_db(
                english_text,
                japanese_text,
                interaction.user.display_name)
            
            if success:
                await interaction.followup.send(
                    f"名言が保存されました:\n```{english_text}\n{japanese_text}```",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    error_message,
                    ephemeral=True
                )
        except Exception as e:
            print(f"モーダル送信エラー: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "モーダル送信の際にエラーが発生しました",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        "モーダル送信の際にエラーが発生しました",
                        ephemeral=True
                    )
            except:
                pass

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(f"モーダルエラー: {error}")
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "モーダル送信の際にエラーが発生しました",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "モーダル送信の際にエラーが発生しました",
                    ephemeral=True
                )
        except:
            pass

# ---コマンド定義---
# /meigen
async def save_meigen_to_db(text_eng, text_jpn, username):
    try:
        # 非同期処理でタイムアウトを避ける
        data = {
            'text_eng': text_eng,
            'text_jpn': text_jpn,
            'username': username,
        }

        # タイムアウト付きでデータベースに保存
        result = await asyncio.wait_for(
            asyncio.to_thread(
                lambda: supabase.table('meigen').insert(data).execute()
            ),
            timeout=10.0
        )
        
        if result.data:
            print(f"名言保存成功: {username} - {text_eng[:50]}...")
            return True, None
        else:
            print(f"名言保存失敗: レスポンスデータが空です")
            return False, "データの保存に失敗しました。"
    
    except asyncio.TimeoutError:
        print("データベース保存タイムアウト")
        return False, "データベースの応答がタイムアウトしました。"
    except Exception as e:
        print("--- データベース保存エラー（トレースバック開始）---")
        traceback.print_exc()
        print("--- データベース保存エラー（トレースバック終了）---")
        
        error_msg = "保存中にエラーが発生しました。"
        if "duplicate" in str(e).lower():
            error_msg = "同じ名言が既に登録されています。"
        elif "connection" in str(e).lower():
            error_msg = "データベースへの接続に失敗しました。"
        
        return False, error_msg