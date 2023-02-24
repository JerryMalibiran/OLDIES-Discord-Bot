import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = []
        self.playing = ''

    async def check_connection(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message('You must be inside a voice call!')
            return False

        voice = get(self.bot.voice_clients, guild=interaction.guild)
        if voice is None:
            await interaction.user.voice.channel.connect()
        elif interaction.user.voice.channel != voice.channel:
            await interaction.response.send_message('I am in a different voice call!')
            return False

        return True

    @app_commands.command(name="play", description="Bored? Play some music in the voice call!")
    async def play(self, interaction: discord.Interaction, url: str):
        status = await self.check_connection(interaction)

        if status:
            self.playing = url
            await interaction.response.send_message(f'Now playing: {self.playing}')

    @app_commands.command(name="next", description="Play next in queue.")
    async def next(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            try:
                self.playing = self.queue.pop(0)
                await interaction.response.send_message(f'Now playing next in queue: {self.playing}')
            except IndexError as e:
                await interaction.response.send_message('Queue is empty!')

    @app_commands.command(name="add", description="Add something to the queue.")
    async def add(self, interaction: discord.Interaction, url: str):
        status = await self.check_connection(interaction)

        if status:
            self.queue.append(url)
            await interaction.response.send_message(f'URL:{url} added to queue!')

    @app_commands.command(name="clear", description="Clear the queue.")
    async def clear(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            self.queue.clear()
            await interaction.response.send_message(f'Queue cleared!')

    @app_commands.command(name="disconnect", description="Disconnect the bot.")
    async def disconnect(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            voice = get(self.bot.voice_clients, guild=interaction.guild)
            await voice.disconnect()
            await interaction.response.send_message(f'Disconnected!')

    @app_commands.command(name="queue", description="Shows the queue.")
    async def queue(self, interaction: discord.Interaction):
        str_queue = 'Queue:'

        for i, val in enumerate(self.queue):
            str_queue += f'\n{i+1}. {val}'

        await interaction.response.send_message(str_queue)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Music(bot)
    )
