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


# use yield and iterate on the result
def find_diff(lst1, lst2):
    ret = None
    for item in lst1:
        if item not in lst2:
            ret = item
    if ret is not None:
        return ret
    for item in lst2:
        if item not in lst1:
            ret = item
    return ret


def notify(members, new_members):
    msg = ""
    try:
        if len(members) < len(new_members):
            msg = find_diff(members, new_members).nick + " נכנס"
        if len(members) > len(new_members):
            msg = find_diff(members, new_members).nick + " עזב"
    except AttributeError:
        print("error")
    msg += " | ("
    for member in new_members:
        msg += member.nick + " "
    msg += str(max(len(members), len(new_members))) + ")"
    bot.send_message(chat_id=USER_ID, text=msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    members = []
    while True:
        # get the channel data
        await client.fetch_channel(CHANNEL_ID)
        channel = client.get_channel(CHANNEL_ID)

        # notify if there is more than one member
        if 1 <= len(channel.members) and channel.members != members:
            notify(members, channel.members)
        members = channel.members


client.run(DISCORD_TOKEN)
