import os
from dotenv import load_dotenv
from bot import DiscordBot
from openaiapi import OpenAIAPI
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')
DISCORD_TOKEN = os.getenv('DISCORD-TOKEN')
# DISCORD_APPLICATION_ID = os.getenv('DISCORD-APPLICATION-ID')
# DISCORD_PUBLIC_KEY = os.getenv('DISCORD-PUBLIC-KEY')

ai = OpenAIAPI(OPENAI_API_KEY)
bot = DiscordBot(ai)
bot.run(DISCORD_TOKEN)
