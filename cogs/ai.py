import discord
from discord.ext import commands
from discord import app_commands


class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chat", description="Talk to an AI. Ask Anything!")
    async def chat(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        response = self.bot.ai.completion(prompt)
        embed = discord.Embed(title="Prompt", description=prompt)
        await interaction.followup.send(content=response, embed=embed)

    @app_commands.command(name="image", description="Create an AI generated image from a text prompt. How about a cat?")
    async def image(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        response = self.bot.ai.generation(prompt)
        embed = discord.Embed(title="Generated Image",
                              description=prompt, url=response)
        embed.set_image(url=response)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        AI(bot)
    )
