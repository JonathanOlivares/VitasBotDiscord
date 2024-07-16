import discord
import asyncio

import utils.useful as useful
from discord.ext import commands
from settings.config import TOKEN

class BotVitas(commands.Bot):
    async def on_ready(self: commands.Bot):
        activity = discord.Game(name="v!help")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"Connected as :{self.user}")

    async def setup_hook(self: commands.Bot):
        self.remove_command("help")
        await useful.load_all(self)
        await self.tree.sync()

        # @bot_vitas.event  # En caso de comando incorrecto
    # async def on_command_error(ctx, error: discord.DiscordException):
    #     if isinstance(error, commands.CommandNotFound):
    #         print(f"User put an incorrect command: {error}")
    #     elif isinstance(error, commands.MissingRequiredArgument):
    #         print(f"User miss argument: {error}")
    #     else:
    #         print(
    #             f"Error no considerado: {error}")


async def main():
    command_prefix = "v!"
    intents = discord.Intents.all()
    description="Vitas"
    bot_vitas = BotVitas(command_prefix=command_prefix, description=description,intents=intents)
    
    if TOKEN is None:
        raise ValueError("Token not found.")

    await bot_vitas.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
