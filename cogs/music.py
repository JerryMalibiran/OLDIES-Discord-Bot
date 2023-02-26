import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
from yt_dlp import YoutubeDL
import os


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = []
        self.playing = ''
        self.dir = os.getcwd()

        ydl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            # bind to ipv4 since ipv6 addresses cause issues sometimes
            # 'source_address': '0.0.0.0',
        }

        self.ffmpeg_options = {
            'options': '-vn',
        }

        self.ydl = YoutubeDL(ydl_format_options)

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
            self.playing = ''
            voice = get(self.bot.voice_clients, guild=interaction.guild)
            if voice.is_playing():
                voice.stop()

            await self.play_audio(url, interaction)

    @app_commands.command(name="next", description="Play next in queue.")
    async def next(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            await self.play_next(interaction)

    @app_commands.command(name="add", description="Add something to the queue.")
    async def add(self, interaction: discord.Interaction, url: str):
        status = await self.check_connection(interaction)

        if status:
            self.queue.append(url)
            await interaction.response.send_message(f'{url} added to queue!')

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

    @app_commands.command(name="current", description="Shows what is currently playing.")
    async def current(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Now playing: {self.playing}')

    @app_commands.command(name="queue", description="Shows the queue.")
    async def queue(self, interaction: discord.Interaction):
        str_queue = 'Queue:'

        for i, val in enumerate(self.queue):
            str_queue += f'\n{i+1}. {val}'

        await interaction.response.send_message(str_queue)

    async def play_audio(self, url: str, interaction: discord.Interaction, next=False, auto=False):
        if not auto:
            await interaction.response.defer()

        loop = self.bot.loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ydl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        song = data['url']
        player = FFmpegPCMAudio(
            song, **self.ffmpeg_options, executable=f'{self.dir}/ffmpeg.exe')

        voice = get(self.bot.voice_clients, guild=interaction.guild)
        voice.play(player, after=lambda e: print(f'Player error: {e}') if e else asyncio.run_coroutine_threadsafe(
            self.play_next(interaction, True), loop))
        self.playing = data['original_url']

        if auto:
            await interaction.channel.send(f'Now playing next in queue: {self.playing}')
        else:
            await interaction.followup.send(f'Now playing next in queue: {self.playing}' if next else f'Now playing: {self.playing}')

    @ app_commands.command(name="pause", description="Pause what's currently playing.")
    async def pause(self, interaction: discord.Interaction):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        voice.pause()
        await interaction.response.send_message("Paused!")

    @ app_commands.command(name="resume", description="Resume what's currently playing.")
    async def resume(self, interaction: discord.Interaction):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        voice.resume()
        await interaction.response.send_message("Resumed!")

    async def play_next(self, interaction: discord.Interaction, auto=False):
        if self.playing == '' and auto:
            return

        try:
            self.playing = self.queue.pop(0)
            voice = get(self.bot.voice_clients, guild=interaction.guild)
            if not auto and voice.is_playing():
                voice.stop()
            await self.play_audio(self.playing, interaction, True, auto)
        except IndexError as e:
            await interaction.response.send_message('Queue is empty!')
            self.playing = ''


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Music(bot)
    )
