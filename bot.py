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

    @bot.command()
    async def image(ctx, *, prompt):
        response = ai.generation(prompt)
        embed = discord.Embed(title="Generated Image",
                              description=prompt, url=response)
        embed.set_image(url=response)
        await ctx.reply(embed=embed)

    bot.run(token)
