import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select


class Dropdown(Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        options = [discord.SelectOption(
            label=cog_name, description=cog.description) for cog_name, cog in self.bot.cogs.items()]
        super().__init__(placeholder='Select a category...',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cog = self.bot.get_cog(self.values[0])
        commands_list = []

        for command in cog.walk_commands():
            commands_list.append(command)

        for command in cog.walk_app_commands():
            commands_list.append(command)

        embed = discord.Embed(title=f'{cog.__cog_name__} Commands',
                              description='\n'.join(
                                  f'**{self.bot.prefix}{command.name}**\n`{command.description}`' for command in commands_list
                              ))

        await interaction.response.send_message(embed=embed, ephemeral=True)


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Are you lost? Get some help.")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title='Help',
            description='Select a category in the options below to check them out.'
        )

        view = View().add_item(Dropdown(self.bot))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.is_owner()
    @app_commands.command(name="sync", description="For syncing bot commands.")
    async def sync(self, interaction: discord.Interaction):
        n = await self.bot.tree.sync()
        await interaction.response.send_message(f'{len(n)} command/s synced.')


async def setup(bot: commands.Bot):
    await bot.add_cog(
        General(bot)
    )
