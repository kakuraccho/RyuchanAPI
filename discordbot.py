# 外部ライブラリからのimport
import discord
import os

from dotenv import load_dotenv
load_dotenv

# botトークンを.envから読み込む
TOKEN = os.getenv('TOKEN')

# discordBotを使うのに必要
intents = discord.Intents.default()
# メッセージ内容を取得するにはこれが必要
intents.message_content = True

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がbotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)