import os
import discord
import yaml

queue = []
now_playing = None  # Song playing

extensions = [
    'commands.music',
    'commands.general',
    'commands.options',
    'commands.interaction'
]

async def bot_send_msg(ctx, msg, type: str = None):
    data = get_data_yaml("settings.yaml")
    channel = get_channel(data,ctx)
    if (type == "embed"):
        await channel.send(embed=msg)
    else:
        await channel.send(msg)

def get_text_in_language(key,command) -> str | dict:
    data = get_data_yaml("settings.yaml")
    lang = data["language"]
    command = get_module_name(command)
    data = get_data_yaml("languages",lang,f"{command}.yaml")
    return data[key]

def get_channel(data,ctx):
    txt_channel = data["textChannel"]
    txt_channel = discord.utils.get(ctx.guild.text_channels, name=txt_channel)
    if (txt_channel == "false" or txt_channel == None):
        channel = ctx
    else:
        channel = txt_channel
    return channel

def get_path(p1,p2="",p3=""):
    help_path = os.path.join("settings",p1,p2,p3)
    path = os.path.abspath(path=help_path)
    return path

def get_data_yaml(p1,p2="",p3=""):
    path = get_path(p1,p2,p3)
    with open(path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

# Load bot commands
async def load(bot):
    global extensions
    for ext in extensions:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(e)
        
# async def unload(lang: str, bot):
#     temp_list = list(map(lambda x: str(lang + "." + x), extensions))
#     for ext in temp_list:
#         try:
#             await bot.unload_extension(ext)
#         except Exception as e:
#             print(e)   

def get_module_name(path):
    name = os.path.basename(path).split('.')[0]
    return name