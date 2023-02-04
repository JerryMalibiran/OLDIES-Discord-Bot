import os
from dotenv import load_dotenv
import bot
from ai import AI
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')
DISCORD_TOKEN = os.getenv('DISCORD-TOKEN')
# DISCORD_APPLICATION_ID = os.getenv('DISCORD-APPLICATION-ID')
# DISCORD_PUBLIC_KEY = os.getenv('DISCORD-PUBLIC-KEY')


ai = AI(OPENAI_API_KEY)
bot.run(DISCORD_TOKEN, ai)
