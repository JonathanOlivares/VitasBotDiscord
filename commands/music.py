# Bot music
import re
import random
import asyncio
import discord
import subprocess
import utils.verify as verify
import utils.useful as useful

from pytube import Search, YouTube
from discord.ext import commands
from enum import Enum


class BotAction(Enum):
    NOTHING = 0
    CONNECT = 1
    MOVE = 2
    FALSE = 3


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str):

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
            useful.queue.append(video)
            vc = ctx.voice_client

            if vc is None:
                raise Exception("Bot is not in a voice channel.")

            if not isinstance(vc, discord.VoiceClient):
                raise TypeError("vc is not a discord.VoiceClient")

            if not vc.is_playing():
                await self.play_next(ctx)
                vc.pause()
                await asyncio.sleep(2)
                vc.resume()

    async def get_video_results(self, ctx: commands.Context, search: str):
        videos: list[YouTube] | None = Search(search).results
        key = "select_option"
        txt_title = useful.get_text_in_language(ctx, key, __file__)

        if not isinstance(txt_title, str):
            raise TypeError("txt_title is not a str. Expected: str")

        if videos is None:
            NotImplemented  # AÑADIR TEXTO QUE DIGA QUE NO SE ENCONTRARON RESULTADOS
            return

        embed = discord.Embed(
            title=txt_title, color=discord.Color.purple())
        for i in range(5):
            author = videos[i].author
            name = videos[i].title
            embed.add_field(
                name=f"{i+1}) {author}", value=name, inline=False)

        await useful.bot_send_msg(ctx, embed)

        try:
            MEJORAR ESTA FORMA DE IMPLEMENTAR, buscar forma sin try except
            response = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=20)
            if (response.content.isdigit() and int(response.content) in range(1, 6)):
                song_number = int(response.content)
                # You can use song_number to play the song
                key = "select_number"
                msg = useful.get_text_in_language(ctx, key, __file__)
                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                msg = msg.format(song_number)
                await useful.bot_send_msg(ctx, msg)
                return videos[song_number-1]
            else:
                key = "invalid_digit"
                msg = useful.get_text_in_language(ctx, key, __file__)
                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                await useful.bot_send_msg(ctx, msg)
                return None
        except asyncio.TimeoutError:
            key = "timeout"
            msg = useful.get_text_in_language(ctx, key, __file__)
            if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
            await useful.bot_send_msg(ctx, msg)
            return None

    # Return True if playing and return false if the queue is empty
    async def play_next(self, ctx: commands.Context):
        vc = ctx.voice_client

        if vc is None:
            raise Exception("Unexpected expeception. VoiceClient is None.")

        if not isinstance(vc, discord.VoiceClient):
            raise TypeError("vc is not a discord.VoiceClient")

        if useful.queue:
            useful.now_playing = useful.queue[0]

            ytdl = subprocess.Popen(
                ["yt-dlp", "-f", "bestaudio/worst", "-i", useful.queue.pop(0).watch_url, "-o", "-"], stdout=subprocess.PIPE)
            
            ystoud = ytdl.stdout

            if ystoud is None:
                raise Exception("Unexpected error. ystoud is None.")
            
            # if not isinstance(ystoud, BufferedIOBase):
            #     raise TypeError("ystoud is not a BufferedIOBase")

            ## cuidado ver si funciona
            source = discord.FFmpegPCMAudio(
                str(ystoud), pipe=True)

            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
                self.after_play(ctx), self.bot.loop))

            embed = discord.Embed(
                title="", color=discord.Color.purple())
            key = "play"
            playing = useful.get_text_in_language(ctx,key, __name__)
            embed.add_field(
                name=f"{playing} {useful.now_playing.author}", value=useful.now_playing.title, inline=False)
            asyncio.run_coroutine_threadsafe(
                useful.bot_send_msg(ctx, embed), self.bot.loop)

            return True
        else:
            key = "no_audio"
            msg = useful.get_text_in_language(ctx, key, __file__)
            if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
            asyncio.run_coroutine_threadsafe(
                useful.bot_send_msg(ctx, msg),
                self.bot.loop)
            useful.now_playing = None
            vc.stop()
            print("Finish queue\n")
            return False

    async def after_play(self, ctx: commands.Context):
        if await self.play_next(ctx):
            vc = ctx.voice_client

            if vc is None:
                raise Exception("Bot is not in a voice channel.")

            if not isinstance(vc, discord.VoiceClient):
                raise TypeError("vc is not a discord.VoiceClient")

            vc.pause()
            await asyncio.sleep(2)
            vc.resume()

    @commands.command()
    async def skip(self, ctx: commands.Context):
        if await verify.verify_music_commands(ctx):
            if useful.now_playing != None:
                useful.now_playing = None
                vc = ctx.voice_client

                if vc is None:
                    raise Exception("Bot is not in a voice channel.")

                if not isinstance(vc, discord.VoiceClient):
                    raise TypeError("vc is not a discord.VoiceClient")

                vc.stop()
            else:
                key = "no_playing"
                msg = useful.get_text_in_language(ctx, key, __file__)

                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if await verify.verify_music_commands(ctx):

            if useful.now_playing != None:
                vc = ctx.voice_client
                if vc is None:
                    raise Exception("Bot is not in a voice channel.")

                if not isinstance(vc, discord.VoiceClient):
                    raise TypeError("vc is not a discord.VoiceClient")

                vc.pause()
            else:
                key = "no_playing"
                msg = useful.get_text_in_language(ctx, key, __file__)

                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if await verify.verify_music_commands(ctx):
            if useful.now_playing != None:
                vc = ctx.voice_client
                if vc is None:
                    raise Exception("Bot is not in a voice channel.")

                if not isinstance(vc, discord.VoiceClient):
                    raise TypeError("vc is not a discord.VoiceClient")

                vc.resume()
            else:
                key = "no_playing"
                msg = useful.get_text_in_language(ctx, key, __file__)

                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if await verify.verify_music_commands(ctx):
            vc = ctx.voice_client

            if vc is None:
                raise Exception("Bot is not in a voice channel.")

            if not isinstance(vc, discord.VoiceClient):
                raise TypeError("vc is not a discord.VoiceClient")

            if vc.is_playing():
                useful.queue.clear()
                vc.stop()
                useful.now_playing = None
            else:
                key = "no_playing"
                msg = useful.get_text_in_language(ctx, key, __file__)
                if not isinstance(msg, str):
                    raise TypeError("msg is not a string type. Expected: str")
                await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def join(self, ctx: commands.Context):  # Requires: pip install pynacl
        is_join = True
        action = await self.verify_join(ctx)
        author = ctx.author
        if author is None:
            raise Exception("Author is None.")

        if not isinstance(author, discord.Member):
            raise TypeError("author is not a discord.Member")

        vc = author.voice

        if vc is None:
            raise Exception("Author is not in a voice channel.")

        channel = vc.channel

        if channel is None:
            raise Exception("Author is not in a voice channel.")

        match action:
            case BotAction.CONNECT:
                await channel.connect()
            case BotAction.MOVE:
                if not isinstance(channel, discord.VoiceChannel):
                    raise TypeError("channel is not a discord.VoiceChannel")
                await self.move_bot(ctx, channel)
            case BotAction.FALSE:
                is_join = False
        return is_join

    async def verify_join(self, ctx: commands.Context):
        author = ctx.author
        if not isinstance(author, discord.Member):
            return BotAction.FALSE
        vc = author.voice
        if vc is None:
            return BotAction.FALSE

        channel = vc.channel
        if verify.author_in_voice_channel(ctx):

            if not isinstance(channel, discord.VoiceChannel):
                return BotAction.FALSE

            if ctx.guild is None:
                return BotAction.FALSE

            bot_voice = ctx.voice_client

            if bot_voice is None:
                return 2

            if not isinstance(bot_voice, discord.VoiceClient):
                return 2

            if not verify.bot_in_voice_channel(ctx):
                return BotAction.CONNECT

            elif bot_voice is not None and bot_voice.is_playing():
                if verify.same_voice_channel(ctx, channel=channel):
                    return BotAction.NOTHING
                else:
                    key = "other_channel"

            elif not verify.same_voice_channel(ctx, channel=channel):
                return BotAction.MOVE

            else:
                return BotAction.NOTHING
        else:
            key = "must_be_in_voice_channel"

        msg = useful.get_text_in_language(ctx, key, __file__)
        if not isinstance(msg, str):
            raise TypeError("msg is not a string type. Expected: str")
        await useful.bot_send_msg(ctx, msg)
        return BotAction.FALSE

    async def move_bot(self, ctx: commands.Context, channel: discord.VoiceChannel):
        vc = ctx.voice_client

        if vc is None:
            raise Exception("Bot is not in a voice channel.")

        if not isinstance(vc, discord.VoiceClient):
            raise TypeError("vc is not a discord.VoiceClient")

        await vc.move_to(channel)
        await verify.verify_move(ctx, channel)
        return True

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        if await verify.verify_music_commands(ctx):
            vc = ctx.voice_client

            if vc is None:
                raise Exception("Bot is not in a voice channel.")

            if not isinstance(vc, discord.VoiceClient):
                raise TypeError("vc is not a discord.VoiceClient")

            useful.queue.clear()
            vc.stop()
        await vc.disconnect()

    @commands.command(name='queue')
    async def queue_command(self, ctx: commands.Context):
        if useful.now_playing != None:
            key = "queue"
            title_txt = useful.get_text_in_language(ctx, key, __file__)
            embed = discord.Embed(
                title=title_txt, color=discord.Color.purple())

            key = "play"
            playing = useful.get_text_in_language(ctx, key, __file__)
            embed.add_field(name=f"{playing} {useful.now_playing.author}",
                            value=useful.now_playing.title, inline=False)
            for i in range(len(useful.queue)):
                author = useful.queue[i].author
                name = useful.queue[i].title
                embed.add_field(
                    name=f"{i+1}) {author}", value=name, inline=False)
            await useful.bot_send_msg(ctx, embed)
        else:
            key = "no_audio"
            msg = useful.get_text_in_language(ctx, key, __file__)
            if not isinstance(msg, str):
                raise TypeError("msg is a dict. Expected: str")
            await useful.bot_send_msg(ctx, msg)

    @commands.command()
    async def shuffle(self, ctx: commands.Context):
        if len(useful.queue) > 0:
            now = useful.now_playing
            if now is None:
                raise Exception("Unexpected error. now is None")
            useful.queue.append(now)
            random.shuffle(useful.queue)
            await self.skip(ctx)
            key = "shuffle"

        else:
            key = "no_songs_to_shuffle"

        msg = useful.get_text_in_language(ctx, key, __file__)
        if not isinstance(msg, str):
            raise TypeError("msg is a dict. Expected: str")
        await useful.bot_send_msg(ctx, msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
