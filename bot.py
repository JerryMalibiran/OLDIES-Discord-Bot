import discord
from discord.ext import commands


def run(token, ai):
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents, command_prefix='/')

    @bot.event
    async def on_ready():
        print(f'Logged in {bot.user} ({bot.user.id})')

    @bot.command()
    async def gpt(ctx, *, prompt):
        response = ai.completion(prompt)
        await ctx.reply(response)

    bot.run(token)
