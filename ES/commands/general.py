import discord

from config import var
from ES.utils import util
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        msg = f"{round(self.bot.latency * 1000)} ms"
        await var.bot_send_msg(ctx, msg)

    @commands.command()
    async def me(self, ctx):
        name = ctx.author.display_name
        await var.bot_send_msg(ctx, f"Tu nombre es: {name}\n")
        await var.bot_send_msg(ctx, "Tu foto de perfil es:")
        await var.bot_send_msg(ctx, "pic", "pic")

    @commands.command()
    async def move(self, ctx, user: discord.Member, channel: discord.VoiceChannel):
        move_bool = True
        print(user)
        if user.voice != None:
            print(self.bot.user)
            if user == self.bot.user and ctx.voice_client.is_playing():
                msg = "El bot actualmente se encuentra en reproducción. Intentelo más tarde"
                await var.bot_send_msg(ctx, msg)
                move_bool = False
            if (move_bool):
                await user.move_to(channel)
                msg = f"{user} fue trasladado al canal de voz {channel}"
                await var.bot_send_msg(ctx, msg)
        else:
            msg = f"El usuario {user} no se encuentra en un canal de voz"
            await var.bot_send_msg(ctx, msg)

    @commands.command()
    async def delete(self, ctx, num):
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
                    await ctx.channel.purge(limit=100)
                    count += 100
                    num %= 100
                await ctx.channel.purge(limit=num)
                count += num

            msg = f"se eliminaron {count} mensajes"
            await var.bot_send_msg(ctx, msg)
        else:
            msg = "No tienes permisos para eliminar mensajes."
            await var.bot_send_msg(ctx, msg)

    @commands.command(name='help')
    async def help_command(self, ctx):
        # Mostrar lista de comandos
        embed = discord.Embed(
            title=f"Comandos", color=discord.Color.purple())
        for command, info in util.commands_help_ES.items():
            embed.add_field(name=command, value=info, inline=False)
        await var.bot_send_msg(ctx, embed, "embed")

    @commands.command()
    async def elvitas(self, ctx):
        vitas = "El Vitas El Vitas"
        for i in range(110):
            vitas += " El Vitas El Vitas"
        await var.bot_send_msg(ctx, vitas)

    @commands.command()
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await var.bot_send_msg(ctx, "Estoy sincronizado")


async def setup(bot):
    await bot.add_cog(General(bot))
