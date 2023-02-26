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
        self.queue = {}
        self.playing = {}

        ydl_format_options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            # bind to ipv4 since ipv6 addresses cause issues sometimes
            # 'source_address': '0.0.0.0'
        }

        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
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
            self.playing[interaction.guild_id] = ''
            self.stop(interaction)

            await self.play_audio(url, interaction)

    @app_commands.command(name="next", description="Play next in queue.")
    async def next(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            if interaction.guild_id not in self.queue:
                self.queue[interaction.guild_id] = []

            if len(self.queue[interaction.guild_id]) < 1:
                await interaction.response.send_message('Queue is empty!')
                return

            voice = get(self.bot.voice_clients, guild=interaction.guild)
            if voice.is_playing():
                self.stop(interaction)
                await interaction.response.send_message('Next audio will be played shortly...')
            else:
                await self.play_next(interaction)

    def stop(self, interaction):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.stop()

    @app_commands.command(name="add", description="Add something to the queue.")
    async def add(self, interaction: discord.Interaction, url: str):
        status = await self.check_connection(interaction)

        if status:
            if interaction.guild.id in self.queue:
                self.queue[interaction.guild_id].append(url)
            else:
                self.queue[interaction.guild_id] = [url]

            await interaction.response.send_message(f'{url} added to queue!')

    @app_commands.command(name="clear", description="Clear the queue.")
    async def clear(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            if interaction.guild.id in self.queue:
                self.queue[interaction.guild_id].clear()
            await interaction.response.send_message(f'Queue cleared!')

    @app_commands.command(name="disconnect", description="Disconnect the bot.")
    async def disconnect(self, interaction: discord.Interaction):
        status = await self.check_connection(interaction)

        if status:
            voice = get(self.bot.voice_clients, guild=interaction.guild)
            self.playing[interaction.guild_id] = ''
            if interaction.guild_id in self.queue:
                self.queue[interaction.guild_id].clear()

            await voice.disconnect()
            await interaction.response.send_message(f'Disconnected!')

    @app_commands.command(name="current", description="Shows what is currently playing.")
    async def current(self, interaction: discord.Interaction):

        if interaction.guild_id not in self.playing:
            self.playing[interaction.guild_id] = ''

        if self.playing[interaction.guild_id] == '':
            audio = 'N/A'
        else:
            audio = self.playing[interaction.guild_id]

        await interaction.response.send_message(f'Now playing: {audio}')

    @app_commands.command(name="queue", description="Shows the queue.")
    async def queue(self, interaction: discord.Interaction):
        if interaction.guild_id not in self.queue:
            self.queue[interaction.guild_id] = []

        str_queue = 'Queue:'

        if len(self.queue[interaction.guild_id]) < 1:
            str_queue += '\nN/A'
        else:
            for i, val in enumerate(self.queue[interaction.guild_id]):
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
            song, **self.ffmpeg_options, executable=f'./ffmpeg.exe')

        voice = get(self.bot.voice_clients, guild=interaction.guild)
        voice.play(player, after=lambda e: print(f'Player error: {e}') if e else asyncio.run_coroutine_threadsafe(
            self.play_next(interaction, True), loop))
        self.playing[interaction.guild_id] = data['original_url']

        if auto:
            await interaction.channel.send(f'Now playing next in queue: {self.playing[interaction.guild_id]}')
        else:
            await interaction.followup.send(f'Now playing next in queue: {self.playing[interaction.guild_id]}' if next else f'Now playing: {self.playing[interaction.guild_id]}')

    @ app_commands.command(name="pause", description="Pause what's currently playing.")
    async def pause(self, interaction: discord.Interaction):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
            await interaction.response.send_message("Paused!")
        else:
            await interaction.response.send_message("Already paused!")

    @ app_commands.command(name="resume", description="Resume what's currently playing.")
    async def resume(self, interaction: discord.Interaction):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        if not voice.is_playing():
            voice.resume()
            await interaction.response.send_message("Resumed!")
        else:
            await interaction.response.send_message("Already resumed!")

    async def play_next(self, interaction: discord.Interaction, auto=False):
        self.playing[interaction.guild_id] = ''
        if len(self.queue[interaction.guild_id]) > 0:
            self.playing[interaction.guild_id] = self.queue[interaction.guild_id].pop(
                0)
            await self.play_audio(self.playing[interaction.guild_id], interaction, True, auto)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Music(bot)
    )
