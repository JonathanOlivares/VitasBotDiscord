import discord

import settings.var as var
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx: commands.Context):
        msg = f"{round(self.bot.latency * 1000)} ms"
        await var.bot_send_msg(ctx, msg)

    @commands.command()
    async def me(self, ctx: commands.Context):
        name = ctx.author.display_name
        pic = ctx.author.avatar
        key = "me"
        msg = var.get_text_in_language(key, __file__).format(name)
        await var.bot_send_msg(ctx,msg)
        await var.bot_send_msg(ctx, msg=pic)

    @commands.command()
    async def move(self, ctx: commands.Context, user: discord.Member, channel: discord.VoiceChannel):
        move_bool = True
        print(user)
        if user.voice != None:
            print(self.bot.user)
            if user == self.bot.user and ctx.voice_client.is_playing():
                key = "playing"
                msg = var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx, msg)
                move_bool = False
            if (move_bool):
                await user.move_to(channel)
                key = "move"
                msg = var.get_text_in_language(key,__file__).format(user,channel)
                await var.bot_send_msg(ctx, msg)
        else:
            key = "not_in_voice"
            msg = var.get_text_in_language(key,__file__).format(user)
            await var.bot_send_msg(ctx, msg)

    @commands.command()
    async def delete(self, ctx: commands.Context, num):
        count = 0
        if ctx.author.guild_permissions.manage_messages:
            if num == "all":
                while True:
                    messages = await ctx.channel.purge(limit=100)
                    count += len(messages)
                    if len(messages) == 0:
                        break
            else:
                num = int(num)
                while (num >= 100):
                    messages = await ctx.channel.purge(limit=100)
                    count += 100
                    num -= messages
                    if len(messages) == 0:
                        break
                await ctx.channel.purge(limit=num)
                count += num

            key = "delete"
            msg = var.get_text_in_language(key,__file__).format(count)
            await var.bot_send_msg(ctx, msg)
        else:
            key = "no_perm"
            msg = var.get_text_in_language(key,__file__)
            await var.bot_send_msg(ctx, key=key,command=__file__)

    @commands.command(name='help')
    async def help_command(self, ctx: commands.Context):
        # Show commands list
        key = "help"
        txt_title = var.get_text_in_language(key,__file__)
        embed = discord.Embed(
            title=txt_title, color=discord.Color.purple())
        key = "commands_help"
        items = var.get_text_in_language(key,__file__).items()
        for command, info in items:
            embed.add_field(name=command, value=info, inline=False)
        await var.bot_send_msg(ctx, msg=embed, type="embed")

    @commands.command()
    async def elvitas(self, ctx):
        vitas = "El Vitas El Vitas"
        for i in range(110):
            vitas += " El Vitas El Vitas"
        await var.bot_send_msg(ctx, vitas)

async def setup(bot):
    await bot.add_cog(General(bot))
