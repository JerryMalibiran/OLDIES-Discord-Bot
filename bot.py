import discord
from discord.ext import commands


def run(token, ai):
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents, command_prefix='/')

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f'Logged in {bot.user} ({bot.user.id})')

    @bot.tree.command(name="gpt", description="Talk to an AI. Ask Anything!")
    async def gpt(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        response = ai.completion(prompt)
        embed = discord.Embed(title="Prompt", description=prompt)
        await interaction.followup.send(content=response, embed=embed)

    @bot.tree.command(name="image", description="Create an AI generated image from a text prompt. How about a cat?")
    async def image(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        response = ai.generation(prompt)
        embed = discord.Embed(title="Generated Image",
                              description=prompt, url=response)
        embed.set_image(url=response)
        await interaction.followup.send(embed=embed)

    bot.run(token)
