import discord
from discord.ext import commands
from discord import app_commands


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play", description="Bored? Play some music in the voice call!")
    async def play(self, interaction: discord.Interaction, url: str):
        if interaction.user.voice is None:
            await interaction.response.send_message('You must be inside a voice call!')


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Music(bot)
    )
