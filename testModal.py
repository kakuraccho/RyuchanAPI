import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ダミーのDB関数（ここを実際のDB処理に置き換え）
async def save_to_db(user_id, text):
    print(f"保存しました: ユーザー {user_id} のテキスト -> {text}")

# モーダル（入力フォーム）クラスを作成
class TextInputModal(discord.ui.Modal, title="テキストを入力してください"):
    text_input = discord.ui.TextInput(label="メッセージ", style=discord.TextStyle.paragraph)

    def __init__(self, user):
        super().__init__()
        self.user = user  # ユーザー情報を保存しておく

    async def on_submit(self, interaction: discord.Interaction):
        # ユーザーがテキストを送信したときに呼ばれる
        user_id = self.user.id
        text = self.text_input.value

        # ここでデータベース保存処理
        await save_to_db(user_id, text)

        # ユーザーに完了メッセージを送る
        await interaction.response.send_message(f"テキストを保存しました: {text}", ephemeral=True)


@bot.tree.command(name="submit", description="テキストをデータベースに登録します")
async def submit(interaction: discord.Interaction):
    # ユーザーにモーダルを送る
    modal = TextInputModal(interaction.user)
    await interaction.response.send_modal(modal)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run("YOUR_BOT_TOKEN")
