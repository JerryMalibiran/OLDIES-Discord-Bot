import os
import discord
from discord.ext import commands
from openaiapi import OpenAIAPI


class DiscordBot(commands.Bot):
    def __init__(self, ai: OpenAIAPI):
        self.ai = ai
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix='/',
            intents=intents
        )

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in {self.user} ({self.user.id})')
