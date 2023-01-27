import json
import os
import discord

queue = []
now_playing = None  # Cancion actualmente sonando

extensions = [
    'commands.music',
    'commands.general',
    'commands.options'
]


async def bot_send_msg(ctx, msg, type: str = None):
    help_path = os.path.join("config", "options.json")
    path = os.path.abspath(path=help_path)
    with open(path) as json_file:
        data = json.load(json_file)

    txt_channel = data["textChannel"]
    txt_channel = discord.utils.get(ctx.guild.text_channels, name=txt_channel)
    if (txt_channel == "false" or txt_channel == None):
        channel = ctx
    else:
        channel = txt_channel

    if (type == "embed"):
        await channel.send(embed=msg)

    else:
        await channel.send(msg)

# Bot commands
async def load(bot):
    help_path = os.path.join("config", "options.json")
    path = os.path.abspath(path=help_path)
    with open(path) as json_file:
        data = json.load(json_file)

    lang = data["language"]
    temp_list = list(map(lambda x: str(lang + "." + x), extensions))
    for ext in temp_list:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(e)
        
async def unload(lang: str, bot):
    temp_list = list(map(lambda x: str(lang + "." + x), extensions))
    for ext in temp_list:
        try:
            await bot.unload_extension(ext)
        except Exception as e:
            print(e)   

