# Discord user can have custom options
import os
import discord
import utils.useful as useful


from discord.ext import commands
from settings.lang import LANG_CODES
from utils.globals import cache

class Options(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.option_dic = {}
        help_path = os.path.join("settings", "settings.yaml")
        self.path = os.path.abspath(path=help_path)

    @commands.command()
    async def options(self, ctx) -> None:
        embed = discord.Embed(
            title=f"Options:", color=discord.Color.purple())
        key = "commands_option"
        texts = useful.get_text_in_language(ctx, key, __file__)

        if not isinstance(texts, dict):
            raise TypeError("texts is not a dict. Expected: dict") 

        items = texts.items()

        for command, info in items:
            embed.add_field(name=command, value=info, inline=False)

        await useful.bot_send_msg(ctx, embed)

    @commands.command()
    async def language(self, ctx: commands.Context, lang: str) -> None:
        if lang in LANG_CODES:
            guild = ctx.guild
            
            if guild is None:
                raise Exception("Must be in a guild to change language.")
                
            server = cache.get_server(guild.name)
            if server is None:
                server = cache.add_server(guild.name)
            
            data = server.get_all_info()
            cache.update_server(data, {"language": lang})

            key = "lang_change"
            msg = useful.get_text_in_language(ctx, key, __file__)

            if not isinstance(msg, str):
                raise TypeError("msg is a dict. Expected: str")
            await useful.bot_send_msg(ctx, msg)

    @commands.command(name="botchannel")
    async def channel_bot_txt(self, ctx: commands.Context, channel_name: str):
        flag_change = True
        guild = ctx.guild
        if guild is None:
                raise Exception("Must be in a guild to change channel.")

        if channel_name != "false":
            channel_name = channel_name.replace(
             "<", "").replace(">", "").replace("#", "")

            channel = discord.utils.get(
                guild.text_channels, 
                name=channel_name
            )

            if channel is None:
                key = "no_channel"
                flag_change = False
            # channel = guild.get_channel(int(channel_name))
            # channel = channel.name
        
        if flag_change:
            key = "channel_change"

        server = cache.get_server(guild.name)

        if server is None:
            server = cache.add_server(guild.name)

        data = server.get_all_info()
        cache.update_server(data, {"channel": channel_name})

        msg = useful.get_text_in_language(ctx, key, __file__)
        if not isinstance(msg, str):
            raise TypeError("msg is a dict. Expected: str")
        await useful.bot_send_msg(ctx, msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(Options(bot))
