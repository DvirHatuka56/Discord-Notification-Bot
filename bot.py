import discord
import telegram
import json


def get_config(path="config.json"):
    with open(path, "r") as reader:
        return json.loads(reader.read())


client = discord.Client()
config = get_config()


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


def notify(members, new_members, bot):
    msg = ""
    try:
        diff_member = find_diff(members, new_members)
        if not diff_member.bot:
            if len(members) < len(new_members):
                msg = diff_member.nick + " נכנס"
            if len(members) > len(new_members):
                msg = diff_member.nick + " עזב"
    except AttributeError:
        print("error")
    msg += " | ("
    for member in new_members:
        if member.bot:
            continue
        msg += member.nick + " "
    msg += str(len(new_members)) + ")"
    for user in config["UserId"]:
        bot.send_message(chat_id=user, text=msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    bot = telegram.Bot(config["TelegramToken"])
    for user in config["UserId"]:
        bot.send_message(chat_id=user,
                         text="Started the bot, you will receive notification when a user connects to discord")
    members = []
    while True:
        # get the channel data
        await client.fetch_channel(config["ChannelId"])
        channel = client.get_channel(config["ChannelId"])

        # notify if there is more than one member
        if 1 <= len(channel.members) and channel.members != members:
            notify(members, channel.members, bot)
        members = channel.members


client.run(config["DiscordToken"])
