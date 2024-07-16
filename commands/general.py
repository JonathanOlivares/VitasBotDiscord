import discord

import utils.useful as useful
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx: commands.Context):
        msg = f"{round(self.bot.latency * 1000)} ms"
        await useful.bot_send_msg(ctx, msg) 

    @commands.command()
    async def me(self, ctx: commands.Context):
        name = ctx.author.display_name
        pic = ctx.author.avatar

        key = "me"
        msg = useful.get_text_in_language(ctx, key, __file__)

        if not isinstance(msg, str):
            raise TypeError("msg is a dict. Expected: str")

        msg = msg.format(name)

        await useful.bot_send_msg(ctx,msg)
        await useful.bot_send_msg(ctx, msg=str(pic))

    @commands.command()
    async def move(self, ctx: commands.Context, user: discord.Member, channel: discord.VoiceChannel):
        print(user)
        if user.voice != None:
            print(self.bot.user)
            vc = ctx.voice_client
            
            if vc is None:
                raise Exception("Bot is not in a voice channel.")
            
            if not isinstance(vc, discord.VoiceClient):
                raise TypeError("vc is not a discord.VoiceClient")

            if user == self.bot.user and vc.is_playing():
                key = "playing"
            else:
                await user.move_to(channel)
                key = "move"
        else:
            key = "not_in_voice"

        msg = useful.get_text_in_language(ctx, key,__file__)
        if not isinstance(msg, str):
            raise TypeError("msg is a dict. Expected: str")
        msg = msg.format(user)
        await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def delete(self, ctx: commands.Context, option: str):
        count = 0
        author = ctx.author

        if not isinstance(author, discord.Member):
            raise TypeError("author is not a discord.Member")

        text_channel = ctx.channel
        if not isinstance(text_channel, discord.TextChannel):
            raise TypeError("Unexpected error. Channel is not a discord.TextChannel.")

        author_can_delete = author.guild_permissions.manage_messages
        if author_can_delete:
            if option == "all":
                while True:
                    messages = await text_channel.purge(limit=100)
                    count += len(messages)
                    if len(messages) == 0:
                        break
            else:
                if not option.isdigit():
                    raise TypeError("num is not a str")
                num = int(option)

                while num >= 100:
                    messages = await text_channel.purge(limit=100)
                    count += 100
                    num -= len(messages)
                    if len(messages) == 0:
                        break
                await text_channel.purge(limit=num)
                count += num
            key = "delete"
        else:
            key = "no_perm"

        msg = useful.get_text_in_language(ctx, key,__file__)
        if not isinstance(msg, str):
            raise TypeError("msg is a dict. Expected: str")
        await useful.bot_send_msg(ctx, msg)

    @commands.command(name='help')
    async def help_command(self, ctx: commands.Context):
        # Show commands list
        key = "help"
        txt_title = useful.get_text_in_language(ctx, key,__file__)
        embed = discord.Embed(
            title=txt_title, color=discord.Color.purple())

        key = "commands_help"
        items = useful.get_text_in_language(ctx, key,__file__)

        if not isinstance(items, dict):
            raise TypeError("items is not a dict")

        items = items.items()
        for command, info in items:
            embed.add_field(name=command, value=info, inline=False)
        await useful.bot_send_msg(ctx, msg=embed)

    @commands.command()
    async def elvitas(self, ctx: commands.Context):
        vitas = "El Vitas El Vitas"
        for i in range(110):
            vitas += " El Vitas El Vitas"
        await useful.bot_send_msg(ctx, vitas)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
