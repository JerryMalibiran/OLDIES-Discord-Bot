import os
import discord
from discord.ext import commands
from openaiapi import OpenAIAPI


class DiscordBot(commands.Bot):
    def __init__(self, ai: OpenAIAPI):
        self.ai = ai
        self.prefix = '/'
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.prefix),
            intents=intents
        )

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        activity = discord.Activity(
            name='/help', type=discord.ActivityType.listening)
        await self.change_presence(activity=activity)
        print(f'Logged in {self.user} ({self.user.id})')
