import settings.var as var
import asyncio


async def verify_music_commands(ctx):
    if ctx.voice_client:
        if author_in_voice_channel(ctx) and same_voice_channel(ctx):
            return True
        else:
            key = "same_voice"
    else:
        key = "not_connected_channel"
    
    msg = var.get_text_in_language(key,__file__)
    await var.bot_send_msg(ctx, msg)

    return False

def author_in_voice_channel(ctx): 
    return True if ctx.author.voice != None else False

def same_voice_channel(ctx,channel):
    return True if channel == ctx.voice_client.channel else False

def bot_in_voice_channel(ctx):
    return False if ctx.voice_client == None else True

async def verify_move(ctx,channel):
    while (not same_voice_channel(ctx,channel)):
        await asyncio.sleep(1)

