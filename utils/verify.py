import utils.useful as useful
import asyncio
import discord
from discord.ext import commands

async def verify_music_commands(ctx: commands.Context) -> bool:
    vc = ctx.voice_client
    if vc:
        channel = vc.channel
        if not isinstance(channel, discord.VoiceChannel):
            raise TypeError("vc is not a discord.VoiceClient")
        
        if author_in_voice_channel(ctx) and same_voice_channel(ctx, channel):
            return True
        else:
            key = "same_voice"
    else:
        key = "not_connected_channel"
    
    msg = useful.get_text_in_language(ctx, key,__file__)

    if not isinstance(msg, str):
        raise TypeError("msg is a dict. Expected: str")
        
    await useful.bot_send_msg(ctx, msg)

    return False

def author_in_voice_channel(ctx: commands.Context) -> bool: 
    author = ctx.author

    if author is None:
        raise Exception("Author is None.")

    if not isinstance(author, discord.Member):
        raise TypeError("author is not a discord.Member")
        
    return True if author.voice != None else False

def same_voice_channel(ctx: commands.Context, channel: discord.VoiceChannel) -> bool:
    vc = ctx.voice_client
    if vc is None:
        raise Exception("Bot is not in a voice channel.")

    return True if channel == vc.channel else False

def bot_in_voice_channel(ctx: commands.Context) -> bool:
    return False if ctx.voice_client == None else True

async def verify_move(ctx: commands.Context , channel: discord.VoiceChannel ) -> None:
    while (not same_voice_channel(ctx,channel)):
        await asyncio.sleep(1)

