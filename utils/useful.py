import os
import discord

from discord.ext import commands
from discord import Embed
from settings.lang import load_lang_modules, load_lang_codes
from utils.globals import cache
from settings.servers import Server
from pytube import YouTube

queue: list[YouTube] = []
now_playing: YouTube | None  = None  # Song playing

EXTENSIONS = [
    'commands.music',
    'commands.general',
    'commands.options',
    'commands.interaction'
]


async def bot_send_msg(ctx: commands.Context, msg: Embed | str) -> None:
    guild = ctx.guild
    if guild is None:
        raise Exception("Must be in a guild to send a message.")

    server = get_or_set_server(guild.name)

    channel_name = server.get_channel()
    channel = get_channel(channel_name, ctx)

    if isinstance(msg, Embed):
        await channel.send(embed=msg)
    else:
        await channel.send(msg)


def get_text_in_language(ctx: commands.Context, key: str, module: str) -> str | dict[str, str]:
    guild = ctx.guild
    if guild is None:
        raise Exception("Must be in a guild.")

    server = get_or_set_server(guild.name)
    lang_code = server.get_language()

    lang = cache.get_language(lang_code)
    if lang is None:
        lang = cache.add_language(lang_code)
    
    module = get_module_name(module)
    return lang.get_text(module, key)

def get_or_set_server(server_name: str) -> Server:
    server = cache.get_server(server_name)
    if server is None:
        server = cache.add_server(server_name)
    return server

def get_channel(channel_name: str, ctx: commands.Context):
    guild = ctx.guild
    if guild is None or channel_name == "false":
        return ctx

    channel = discord.utils.get(
        guild.text_channels, name=channel_name)

    if channel is None:
        return ctx

    return channel

# Load bot commands
async def load_bot_extensions(bot: commands.Bot) -> None:
    global EXTENSIONS
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(e)


async def load_all(bot: commands.Bot) -> None:
    await load_bot_extensions(bot)
    load_lang_codes()
    load_lang_modules()

def get_module_name(path):
    name = os.path.basename(path).split('.')[0]
    return name
# async def unload(lang: str, bot):
#     temp_list = list(map(lambda x: str(lang + "." + x), extensions))
#     for ext in temp_list:
#         try:
#             await bot.unload_extension(ext)
#         except Exception as e:
#             print(e)
