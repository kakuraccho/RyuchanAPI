import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# ---環境変数---
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_TOKEN = os.getenv('SUPABASE_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

# ---環境変数のチェック---
if not all([DISCORD_BOT_TOKEN, SUPABASE_URL, SUPABASE_TOKEN, GUILD_ID]):
    raise ValueError("環境変数に異常があります")

# supabaseクライアント
supabase = create_client(SUPABASE_URL, SUPABASE_TOKEN)

# イベントループの最適化
if hasattr(asyncio, 'set_event_loop_policy'):
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())