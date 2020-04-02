import discord
import telegram

DISCORD_TOKEN = 'DISCORD_TOKEN'
TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
USER_ID = 12312312  # the telegram chat or user id to send the notification to
SERVER_ID = 1111111111111111111  # the discord server id
CHANNEL_ID = 111111111111111111  # the discord channel id (inside the server)

client = discord.Client()
bot = telegram.Bot(TELEGRAM_TOKEN)
bot.send_message(chat_id=USER_ID, text="Started the bot, you will receive notification when a user connects to "
                                         "discord")


def notify(members):
    msg = ""
    for member in members:
        msg += member.nick + " "
    msg += "are talking"
    bot.send_message(chat_id=USER_ID, text=msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    members = 0
    while True:
        # get the channel data
        await client.fetch_channel(CHANNEL_ID)
        channel = client.get_channel(CHANNEL_ID)

        # notify if there is more than one member
        if 1 <= len(channel.members) != members:
            notify(channel.members)
        members = len(channel.members)


client.run(DISCORD_TOKEN)

