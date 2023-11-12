# Discord user can have custom options
import os
import discord
import asyncio
import yaml

from discord.ext import commands
import settings.var as var

class Options(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.option_dic = {}
        self.valid_language = ["US", "ES"]
        help_path = os.path.join("settings", "settings.yaml")
        self.path = os.path.abspath(path=help_path)

    @commands.command()
    async def options(self, ctx):
        embed = discord.Embed(
            title=f"Options:", color=discord.Color.purple())
        key = "commands_option"
        items = var.get_text_in_language(key,__file__).items()
        for command, info in items:
            embed.add_field(name=command, value=info, inline=False)
        await var.bot_send_msg(ctx, embed, "embed")

    @commands.command()
    async def language(self, ctx, lang: str):
        if lang in self.valid_language:
            with open(self.path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)

            data["language"] = lang

            with open(self.path, 'w') as yaml_file:
                yaml.safe_dump(data,yaml_file)

            key = "lang_change"
            msg = var.get_text_in_language(key,__file__)
            await var.bot_send_msg(ctx, msg)

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
            key = "no_channel"
        else:
            with open(self.path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)

            data["textChannel"] = channel
            with open(self.path, 'w') as yaml_file:
                yaml.safe_dump(data,yaml_file)
            key ="channel_change"
            
        msg = var.get_text_in_language(key,__file__)
        await var.bot_send_msg(ctx, msg)

async def setup(bot):
    await bot.add_cog(Options(bot))
