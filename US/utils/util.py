from config import var

commands_help_US = {
    'elvitas': 'The bot sends several messages saying El Vitas',
    'join': 'Join the voice channel of the user executing the command',
    'move':  'Move a @user to another voice channel. Usage: v!move @username voice_channel_name',
    'leave': 'Leave current voice channel',
    'play': 'Plays audio from a specific url or word, if it is a word, the number of the corresponding option must be indicated. Usage: v!play url',
    'skip': 'Skip to the next audio in the queue',
    'queue': 'Show the audios in the queue',
    'shuffle': 'Shuffle the queue by changing the playback order',
    'stop':  'Stop playing bot audios',
    'ping':  'Shows the latency of the bot',
    'me': 'Show your username and avatar',
    'help': 'Show this help',
    'delete': '(User requires permission to delete messages) deletes messages within the channel being invoked. You must indicate the number of messages to delete, if you want to delete all use all. Usage example: v!play delete number',
    'options': 'Show option commands'
}

commands_option_US = {
    'language': 'Change the language of the bot, the language must be specified. Allowed languages: US, ES. Example: v!language US',
    'botchannel': 'Specifies a text channel in which the bot sends messages, to deactivate it, just give false. Example: v!botchannel false'
}


async def verify(ctx):
    if ctx.voice_client:
        if ctx.author.voice != None and ctx.author.voice.channel == ctx.voice_client.channel:
            return True
        else:
            msg = "We must be on the same voice channel"
            await var.bot_send_msg(ctx, msg)
    else:
        msg = "I am not connected to a voice channel."
        await var.bot_send_msg(ctx, msg)

    return False
