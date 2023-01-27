# Bot music
import re
import random
import asyncio
import discord
import subprocess

from pytube import Search, YouTube
from discord.ext import commands
from US.utils.util import verify
from config import var


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, search):
        pattern = re.compile(
            r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
        if (pattern.match(search)):
            video = YouTube(search)
        else:
            video = await self.get_video_results(ctx, search)
            if video == None:
                return "User dont put number"

        if await self.join(ctx):
            var.queue.append(video)  # agrega cancion a la cola
            if not ctx.voice_client.is_playing():
                self.play_next(ctx)

                # Para evitar que el audio comience rapido
                ctx.voice_client.pause()
                await asyncio.sleep(2)
                ctx.voice_client.resume()

    async def get_video_results(self, ctx, search):
        videos = Search(search).results
        embed = discord.Embed(
            title=f"Select the option", color=discord.Color.purple())
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
                msg = f"You selected number {song_number}"
                await var.bot_send_msg(ctx,msg)
                return videos[song_number-1]
            else:
                await var.bot_send_msg(ctx,"A digit between 1 and 5 was expected. Please try again")
                return None
        except asyncio.TimeoutError:
            msg = ("You took too long to respond.")
            await var.bot_send_msg(ctx,msg)
            return None

    def play_next(self, ctx):
        if var.queue:
            var.now_playing = var.queue[0]

            ytdl = subprocess.Popen(
                ["youtube-dl", "-f", "bestaudio/worst", "-i", var.queue.pop(0).watch_url, "-o", "-"], stdout=subprocess.PIPE)
            source = discord.FFmpegPCMAudio(
                ytdl.stdout, pipe=True)

            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))

            embed = discord.Embed(
                title="", color=discord.Color.purple())
            embed.add_field(
                name=f"Playing: {var.now_playing.author}", value=var.now_playing.title, inline=False)
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,embed,"embed"), self.bot.loop)

        else:
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,"There are no more audios in the queue."),
                self.bot.loop)
            var.now_playing = None

    @commands.command()
    async def skip(self, ctx):
        if await verify(ctx):
            if var.now_playing != None:
                ctx.voice_client.stop()
                var.now_playing = None
                ctx.voice_client.pause()
                await asyncio.sleep(2)
                ctx.voice_client.resume()
                

            else:
                msg="There is no song playing."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def stop(self, ctx):
        if await verify(ctx):
            if ctx.voice_client.is_playing():
                var.queue.clear()
                ctx.voice_client.stop()
                var.now_playing = None
            else:
                msg = "There is no song playing."
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def join(self, ctx):  # Es necesario: pip install pynacl
        if ctx.author.voice != None:
            user_voice_channel = ctx.author.voice.channel
        else:
            msg="You must be on a voice channel"
            await var.bot_send_msg(ctx,msg)
            return False
        cv = ctx.voice_client
        if user_voice_channel:
            if cv == None:
                await user_voice_channel.connect()
                return True
            elif not cv.is_playing():
                if cv.channel != user_voice_channel:
                    await cv.move_to(user_voice_channel)
                    while (cv.channel != user_voice_channel):
                        await asyncio.sleep(1)
                return True
            else:  # si esta sonando
                if cv.channel != user_voice_channel:
                    return False
                else:
                    return True
        else:
            msg = "You are not connected to a voice channel"
            await var.bot_send_msg(ctx,msg)
            return False

    @commands.command()
    async def leave(self, ctx):
        if await verify(ctx):
            var.queue.clear()
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(name='queue')
    async def queue_command(self, ctx):
        print(var.now_playing)
        if (var.now_playing != None):
            embed = discord.Embed(
                title=f"Queue:", color=discord.Color.purple())
            embed.add_field(name=f"Playing: {var.now_playing.author}",
                            value=var.now_playing.title, inline=False)
            for i in range(len(var.queue)):
                author = var.queue[i].author
                name = var.queue[i].title
                embed.add_field(
                    name=f"{i+1}) {author}", value=name, inline=False)
            await var.bot_send_msg(ctx,embed,"embed")
        else:
            msg = "There are no songs in the queue"
            await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def shuffle(self, ctx):
        if len(var.queue) > 0:
            var.queue.append(var.now_playing)
            random.shuffle(var.queue)
            await self.skip(ctx)
            msg = "Shuffled"
            await var.bot_send_msg(ctx,msg)
        else:
            msg = "You don't have songs to shuffle"
            await var.bot_send_msg(ctx,msg)


async def setup(bot):
    await bot.add_cog(Music(bot))
