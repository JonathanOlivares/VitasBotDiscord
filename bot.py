import discord
import asyncio

from config import var
from discord.ext import commands
from config.config import TOKEN


def main():
    bot_vitas = commands.Bot(command_prefix="v!",
                             intents=discord.Intents.all(), description="Bot de vitassss")

    bot_vitas.remove_command("help")

    @bot_vitas.event
    async def on_ready():
        await var.load(bot_vitas)
        await asyncio.sleep(2)
        await bot_vitas.tree.sync()
        activity = discord.Game(name="v!help")
        await bot_vitas.change_presence(status=discord.Status.online, activity=activity)
        print(f"Conectado como:{bot_vitas.user}")

    @bot_vitas.tree.command(name="vitas_help", description="Obtienes el comando de ayuda")
    async def vitas_help(interaction: discord.Interaction):
        await interaction.response.send_message("usa v!help para obtener los comandos", ephemeral=True)

    # @bot_vitas.event  # En caso de comando incorrecto
    # async def on_command_error(ctx, error: discord.DiscordException):
    #     if isinstance(error, commands.CommandNotFound):
    #         print(f"User put an incorrect command: {error}")
    #     elif isinstance(error, commands.MissingRequiredArgument):
    #         print(f"User miss argument: {error}")
    #     else:
    #         print(
    #             f"Error no considerado: {error}")

    bot_vitas.run(TOKEN)


if __name__ == "__main__":
    main()
