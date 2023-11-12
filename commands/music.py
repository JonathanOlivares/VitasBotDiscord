# Bot music
import re
import random
import asyncio
import discord
import subprocess
import utils.util as util
from pytube import Search, YouTube
from discord.ext import commands

import settings.var as var
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
    async def play(self, ctx: commands.Context, *, search):

        pattern = re.compile(
            r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
        is_Link = pattern.match(search)
        if (is_Link):
            video = YouTube(search)
        else:
            video = await self.get_video_results(ctx, search)
            if video == None:
                print("User dont put number")
                return 

        if await self.join(ctx):
            var.queue.append(video)
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
                ctx.voice_client.pause()
                await asyncio.sleep(2)
                ctx.voice_client.resume()

    async def get_video_results(self, ctx: commands.Context, search):
        videos = Search(search).results
        key = "select_option"
        txt_title = var.get_text_in_language(key,__file__)
        embed = discord.Embed(
            title=txt_title, color=discord.Color.purple())
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
                key = "select_number"
                msg = var.get_text_in_language(key,__file__).format(song_number)
                await var.bot_send_msg(ctx,msg)
                return videos[song_number-1]
            else:
                key = "invalid_digit"
                msg = var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx,msg)
                return None
        except asyncio.TimeoutError:
            key = "timeout"
            msg = var.get_text_in_language(key,__file__)
            await var.bot_send_msg(ctx,msg)
            return None

    #Return True if playing and return false if the queue is empty
    async def play_next(self, ctx: commands.Context):
        if var.queue:
            var.now_playing = var.queue[0]

            ytdl = subprocess.Popen(
                ["yt-dlp", "-f", "bestaudio/worst", "-i", var.queue.pop(0).watch_url, "-o", "-"], stdout=subprocess.PIPE)
            source = discord.FFmpegPCMAudio(
                ytdl.stdout, pipe=True)

            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.after_play(ctx),self.bot.loop))
            
            embed = discord.Embed(
                title="", color=discord.Color.purple())
            key = "play"
            playing = var.get_text_in_language(key,__name__)
            embed.add_field(
                name=f"{playing} {var.now_playing.author}", value=var.now_playing.title, inline=False)
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,embed,"embed"), self.bot.loop)

            return True
        else:
            key = "no_audio"
            msg = var.get_text_in_language(key,__file__)
            asyncio.run_coroutine_threadsafe(
                var.bot_send_msg(ctx,msg),
                self.bot.loop)
            var.now_playing = None
            ctx.voice_client.stop() 
            print("Finish queue\n")
            return False


    async def after_play(self,ctx):
        if await self.play_next(ctx):
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
                key = "no_playing"
                msg= var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def pause(self, ctx):
        if await util.verify(ctx):
            if var.now_playing != None:
                ctx.voice_client.pause()
            else:
                key = "no_playing"
                msg= var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def resume(self, ctx):
        if await util.verify(ctx):
            if var.now_playing != None:
                ctx.voice_client.resume()
            else:
                key = "no_playing"
                msg= var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def stop(self, ctx):
        if await util.verify(ctx):
            if ctx.voice_client.is_playing():
                var.queue.clear()
                ctx.voice_client.stop()
                var.now_playing = None
            else:
                key = "no_playing"
                msg= var.get_text_in_language(key,__file__)
                await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def join(self, ctx):  # Requires: pip install pynacl
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

    async def verify_join(self,ctx: commands.Context):
        channel = ctx.author.voice.channel
        if(util.author_in_voice_channel(ctx)):
            bot_voice = ctx.voice_client
            if not util.bot_in_voice_channel(ctx):
                return BotAction.CONNECT

            elif bot_voice.is_playing():
                if util.same_voice_channel(ctx,channel=channel):
                    return BotAction.NOTHING
                else:
                    key = "other_channel"

            elif not util.same_voice_channel(ctx,channel=channel):
                return BotAction.MOVE
 
            else:
                return BotAction.NOTHING
        else:
            key="must_be_in_voice_channel"

        msg = var.get_text_in_language(key,__file__)
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
        key = "queue"
        title_txt = var.get_text_in_language(key,__file__)
        if (var.now_playing != None):
            embed = discord.Embed(
                title=title_txt, color=discord.Color.purple())
            
            key = "play"
            playing  = var.get_text_in_language(key,__file__)
            embed.add_field(name=f"{playing} {var.now_playing.author}",
                            value=var.now_playing.title, inline=False)
            for i in range(len(var.queue)):
                author = var.queue[i].author
                name = var.queue[i].title
                embed.add_field(
                    name=f"{i+1}) {author}", value=name, inline=False)
            await var.bot_send_msg(ctx,embed,"embed")
        else:
            key = "no_audio"
            msg = var.get_text_in_language(key,__file__)
            await var.bot_send_msg(ctx,msg)

    @commands.command()
    async def shuffle(self, ctx):
        if len(var.queue) > 0:
            var.queue.append(var.now_playing)
            random.shuffle(var.queue)
            await self.skip(ctx)
            key = "shuffle"

        else:
            key = "no_songs_to_shuffle"
            
        msg = var.get_text_in_language(key,__file__)
        await var.bot_send_msg(ctx,msg)

async def setup(bot):
    await bot.add_cog(Music(bot))
