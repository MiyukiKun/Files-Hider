import os
from telethon import TelegramClient
from pymongo import MongoClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
db_url = os.environ.get('MONGO_DB_URL')
database_channel = int(os.environ.get('DATABASE_CHANNEL'))
bot_username = os.environ.get('BOT_USERNAME')
owner_id = int(os.environ.get('OWNER_ID'))
feedback_group_id = int(os.environ.get('FEEDBACK_GROUP_ID'))
links_database = int(os.environ.get('LINKS_DUMP_CHANNEL'))


client = MongoClient(db_url, tls=True)


bot = TelegramClient(
        'bot', 
        api_id, 
        api_hash, 
    ).start(bot_token=bot_token)