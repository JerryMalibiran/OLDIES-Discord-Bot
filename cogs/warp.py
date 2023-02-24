import discord
from discord.ext import commands
from discord import app_commands
from string import ascii_letters, digits
from random import choice
from json import dumps
from datetime import datetime
import urllib.request


class Warp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def genString(self, stringLength):
        try:
            letters = ascii_letters + digits
            return ''.join(choice(letters) for i in range(stringLength))
        except Exception as error:
            print(error)

    def digitString(self, stringLength):
        try:
            digit = digits
            return ''.join((choice(digit) for i in range(stringLength)))
        except Exception as error:
            print(error)

    @app_commands.command(name="warp-help", description="Add 1GB data to your warp account!")
    async def warp_help(self, interaction: discord.Interaction):
        await interaction.response.send_message("In order to data to your warp+ account, (in the warp application) simply go to Settings > Preferences > General > copy \"Device ID\" and use it with the \"/add-data\" command.")

    @app_commands.command(name="add-data", description="Add 1GB data to your warp account!")
    async def add_data(self, interaction: discord.Interaction, device_id: str):
        await interaction.response.defer()

        url = f"https://api.cloudflareclient.com/v0a{self.digitString(3)}/reg"

        try:
            install_id = self.genString(22)
            body = {
                "key": "{}=".format(self.genString(43)),
                "install_id": install_id,
                "fcm_token": "{}:APA91b{}".format(install_id, self.genString(134)),
                "referrer": device_id,
                "warp_enabled": False,
                "tos": datetime.now().isoformat()[:-3] + "+02:00",
                "type": "Android",
                "locale": "es_ES"
            }
            data = dumps(body).encode("utf8")
            headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "Host": "api.cloudflareclient.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.10.0"
            }
            req = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(req)
            status_code = response.getcode()
        except Exception as error:
            await interaction.followup.send(f"An error happened while adding 1GB data to {device_id}. Make sure your Device ID is correct! Error: {error}")

        if status_code == 200:
            await interaction.followup.send(f"1GB added to {device_id}!")
        else:
            await interaction.followup.send(f"Failed adding 1GB to {device_id}. Try again after a while.")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Warp(bot)
    )
