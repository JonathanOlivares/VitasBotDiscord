# Discord user can have custom options
import json
import os
import discord
import asyncio

from config import var
from discord.ext import commands
from US.utils import util


class Options(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.option_dic = {}
        self.valid_language = ["US", "ES"]
        help_path = os.path.join("config", "options.json")
        self.path = os.path.abspath(path=help_path)

    @commands.command()
    async def options(self, ctx):
        embed = discord.Embed(
            title=f"Options:", color=discord.Color.purple())
        for command, info in util.commands_option_US.items():
            embed.add_field(name=command, value=info, inline=False)
        await var.bot_send_msg(ctx, embed, "embed")

    @commands.command()
    async def language(self, ctx, lang: str):
        if lang in self.valid_language:
            with open(self.path) as json_file:
                data = json.load(json_file)
            data["language"] = lang
            with open(self.path, 'w') as json_file:
                json.dump(data, json_file)

            await var.unload("US", self.bot)
            await asyncio.sleep(2)
            await var.load(self.bot)
            await var.bot_send_msg(ctx, "Language changed.")

    @commands.command(name="botchannel")
    async def channel_bot_txt(self, ctx, channel_name: str):
        if channel_name != "false":
            channel = discord.utils.get(
                ctx.guild.text_channels, name=channel_name)
            if (channel == None):
                try:
                    channel = str(channel_name).replace(
                        "<", "").replace(">", "").replace("#", "")
                    channel = ctx.guild.get_channel(int(channel))
                    channel = channel.name

                except Exception as e:
                    channel = None
                    print(e)
            else:
                channel = channel.name
        else:
            channel = channel_name

        if channel == None:
            msg = "The entered text channel does not exist"
            await var.bot_send_msg(ctx, msg)
        else:
            with open(self.path) as json_file:
                data = json.load(json_file)
            data["textChannel"] = channel
            with open(self.path, 'w') as json_file:
                json.dump(data, json_file)


async def setup(bot):
    await bot.add_cog(Options(bot))
