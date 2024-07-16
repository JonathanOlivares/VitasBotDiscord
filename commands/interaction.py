from discord.ext import commands
import discord

class Interaction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_menu_time = discord.app_commands.ContextMenu(
            name="Get time server of this user",
            callback=self.get_time_on_server,
        )

        self.ctx_menu_giveme = discord.app_commands.ContextMenu(
            name="givemebadge",
            callback=self.givemebadge,
        )

        self.bot.tree.add_command(self.ctx_menu_giveme)
        self.bot.tree.add_command(self.ctx_menu_time)


    async def givemebadge(self,interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message(f'https://discord.com/developers/active-developer', ephemeral=True)

    async def get_time_on_server(self,interaction: discord.Interaction, user: discord.Member):
        name_clicked = user.name if user.bot else user.global_name
        joined_at = user.joined_at
        interaction_guild = interaction.guild
        if joined_at is None or interaction_guild is None:
            raise Exception("Unexcepted error. User joined_at is None or guild is None.")

        msg = f'Hola **{interaction.user.global_name}**. {name_clicked} es miembro de "{interaction_guild.name}" desde {joined_at.strftime("%d-%m-%Y")}'
        await interaction.response.send_message(msg, ephemeral=True)
    
    @discord.app_commands.command(name="givemebadge")
    async def badge(self,interaction: discord.Interaction):
        await interaction.response.send_message("https://discord.com/developers/active-developer", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Interaction(bot))
