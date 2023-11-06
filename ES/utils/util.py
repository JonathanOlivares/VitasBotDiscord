from config import var
import asyncio


commands_help_ES = {
    'elvitas': 'Envia varios mensajes diciendo El Vitas',
    'join': 'Unirse al canal de voz del usuario que ejecuta el comando',
    'move':  'Mover un @usuario a  otro canal de voz. Uso: v!move @usuario  nombre_canal_de_voz',
    'leave': 'Dejar el canal de voz actual',
    'play': 'Reproduce audio desde una url o palabra especificada, en caso de ser una palabra se debe indicar el numero de la opcion correspondiente. Uso: v!play url',
    'skip': 'Salta al siguiente audio en la cola',
    'queue': 'Muestra  los  audios en la cola',
    'shuffle': 'Mezcla la cola cambiando el orden de reproduccion',
    'stop':  'Detener la reproducción de audios del bot',
    'ping':  'Muestra la latencia del bot',
    'me': 'Muestra tu nombre de usuario y tu avatar',
    'help': 'Muestra esta ayuda',
    'delete': '(Usuario requiere tener permisos para borrar mensajes)  elimina mensajes dentro del canal que se invoca.   Se debe indicar el numero de mensajes a eliminar, en caso   de querer borrar todos se usa all.  Ejemplo de uso: v!play delete numero',
    'options': 'Muestra los comandos de opciones'
}

commands_option_ES = {
    'language': 'Cambia el idioma del bot, se debe especificar el idioma. Idiomas permitidos: US,ES. Ejemplo: v!language ES',
    'botchannel': 'Especifica un canal de texto en el cual el bot envia mensajes, para desactivarlo basta con dar false. Ejemplo: v!botchannel false'
}


async def verify_music_commands(ctx):
    if ctx.voice_client:
        if author_in_voice_channel(ctx) and same_voice_channel(ctx):
            return True
        else:
            msg = "Debemos estar en el mismo canal de voz"
            await var.bot_send_msg(ctx, msg)
    else:
        msg = "No estoy conectado a un canal de voz."
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

