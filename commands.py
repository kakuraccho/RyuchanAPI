import asyncio
from supabase import create_client

# ---supabaseに名言を保存---
async def save_meigen_to_db(supabase_client, text, user_id, username, guild_id):
    try:
        result = await supabase_client.table('meigen').insert({
            'text': text,
            'user_id': str(user_id),
            'username': username,
            'guild_id': str(guild_id)
        }).execute

        return True, None
    
    except Exception as e:
        print(f"データベース保存エラー: {e}")
        return False, "保存中にエラーが発生しました"