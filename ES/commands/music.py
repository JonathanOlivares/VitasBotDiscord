# Bot music
import re
import random
import asyncio
import discord
import subprocess
import ES.utils.util as util
from pytube import Search, YouTube
from discord.ext import commands

from config import var
from enum import Enum


class BotAction(Enum):
    NOTHING = 0
    CONNECT = 1
    MOVE = 2
    FALSE = 3

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def play(self, ctx, *, search):

        pattern = re.compile(
            r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
        is_Link = pattern.match(search)
        if (is_Link):
            video = YouTube(search)
        else:
            video = await self.get_video_results(ctx, search)
            if video == None:
                return "User dont put number"

        if await self.join(ctx):
            var.queue.append(video)
            if not ctx.voice_client.is_playing():
                self.play_next(ctx)
                ctx.voice_client.pause()
                await asyncio.sleep(2)
                ctx.voice_client.resume()

    async def get_video_results(self, ctx, search):
        videos = Search(search).results
        embed = discord.Embed(
            title=f"Selecciona la opcion", color=discord.Color.purple())
        for i in range(5):
            author = videos[i].author
            name = videos[i].title
            embed.add_field(
                name=f"{i+1}) {author}", value=name, inline=False)

        await var.bot_send_msg(ctx,embed,"embed")

        try:
            response = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=20)
            if(response.content.isdigit() and int(response.content) in range(1, 6)):
                song_number = int(response.content)
                # You can use song_number to play the song
                msg = f"Seleccionaste el numero {song_number}"
                await var.bot_send_msg(ctx,msg)
                return videos[song_number-1]
            else:
                await var.bot_send_msg(ctx,"Se esperaba un digito entre 1 y 5. Vuelve a intentarlo")
                return None
        except asyncio.TimeoutError:
            msg = ("Te demoraste demaciado en responder.")
            await var.bot_send_msg(ctx,msg)
            return None

    def play_next(self, ctx):
        if var.queue:
            var.now_playing = var.queue[0]

            ytdl = subprocess.Popen(
                ["yt-dlp", "-f", "bestaudio/worst", "-i", var.queue.pop(0).watch_url, "-o", "-"], stdout=subprocess.PIPE)
            source = discord.FFmpegPCMAudio(
                ytdl.stdout, pipe=True)

            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.after_play(ctx),self.bot.loop))
            
            embed = discord.Embed(
                title="", color=discord.Color.purple())
            embed.add_field(
                name=f"Sonando: {var.now_playing.author}", value=var.now_playing.title, inline=False)
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,embed,"embed"), self.bot.loop)

        else:
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,"No hay más audios en la cola."),
                self.bot.loop)
            var.now_playing = None

    async def after_play(self,ctx):
        self.play_next(ctx)
        ctx.voice_client.pause()
        await asyncio.sleep(2)
        ctx.voice_client.resume()
                

    @commands.command()
    async def skip(self, ctx):
        if await util.util.verify(ctx):
            if var.now_playing != None:
                var.now_playing = None
                ctx.voice_client.stop()
            else:
                msg="No hay ninguna canción en reproducción."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def pause(self, ctx):
        if await util.verify(ctx):
            if var.now_playing != None:
                ctx.voice_client.pause()
            else:
                msg="No hay ninguna canción en reproducción."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def resume(self, ctx):
        if await util.verify(ctx):
            if var.now_playing != None:
                ctx.voice_client.resume()
            else:
                msg="No hay ninguna canción en reproducción."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def stop(self, ctx):
        if await util.verify(ctx):
            if ctx.voice_client.is_playing():
                var.queue.clear()
                ctx.voice_client.stop()
                var.now_playing = None
            else:
                msg = "No hay ninguna canción en reproducción."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def join(self, ctx):  # Es necesario: pip install pynacl
        is_join = True
        action = await self.verify_join(ctx)
        match action:
            case BotAction.CONNECT:
                await ctx.author.voice.channel.connect()
            case BotAction.MOVE:
                self.move_bot(ctx.author.voice.channel)
            case BotAction.FALSE:
                is_join = False
        return is_join

    async def verify_join(self,ctx):
        if(util.author_in_voice_channel(ctx)):
            bot_voice = ctx.voice_client
            if not util.bot_in_voice_channel(ctx):
                return BotAction.CONNECT

            elif bot_voice.is_playing():
                if util.same_voice_channel:
                    return BotAction.NOTHING
                else:
                    msg="Bot en otro canal."

            elif not util.same_voice_channel(ctx):
                return BotAction.MOVE
 
            else:
                msg="Bot ya se encuentra en este canal."
        else:
            msg="Debes estar en un canal de voz"

        await var.bot_send_msg(ctx,msg)
        return BotAction.FALSE

    async def move_bot(self, ctx, channel):
        bot_voice = ctx.voice_client
        await bot_voice.move_to(channel)
        await util.verify_move(ctx,channel)
        return True


    @commands.command()
    async def leave(self, ctx):
        if await util.verify(ctx):
            var.queue.clear()
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(name='queue')
    async def queue_command(self, ctx):
        print(var.now_playing)
        if (var.now_playing != None):
            embed = discord.Embed(
                title=f"Cola:", color=discord.Color.purple())
            embed.add_field(name=f"Sonando: {var.now_playing.author}",
                            value=var.now_playing.title, inline=False)
            for i in range(len(var.queue)):
                author = var.queue[i].author
                name = var.queue[i].title
                embed.add_field(
                    name=f"{i+1}) {author}", value=name, inline=False)
            await var.bot_send_msg(ctx,embed,"embed")
        else:
            msg = "No hay canciones en la cola"
            await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def shuffle(self, ctx):
        if len(var.queue) > 0:
            var.queue.append(var.now_playing)
            random.shuffle(var.queue)
            await self.skip(ctx)
            msg = "Mezclado"
            await var.bot_send_msg(ctx,msg)
        else:
            msg = "No posees canciones que mezclar"
            await var.bot_send_msg(ctx,msg)


async def setup(bot):
    await bot.add_cog(Music(bot))
