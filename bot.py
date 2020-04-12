import discord
import telegram
import json
import handler
import logger

CONFIG_PATH = "Files/config.json"


def get_config(path=CONFIG_PATH):
    with open(path, "r") as reader:
        return json.loads(reader.read())


client = discord.Client()
config = get_config()
last_messages = {}


def notify(members, new_members, bot, channel):
    for user in [*handler.settings]:
        message = handler.get_message(user, channel, members, new_members)
        if message == "":
            continue
        if user not in [*last_messages]:
            last_messages[user] = ""
        if message == last_messages[user]:
            continue
        bot.send_message(chat_id=handler.settings[user]["TelegramId"], text=message)
        logger.log(f"(to {user}) {message}")
        last_messages[user] = message


def get_data(members):
    data = []
    for member in members:
        data.append({
            "name": member.name,
            "bot": member.bot
        })
    return data


def equals(a: dict, b: dict):
    try:
        for key in a.keys():
            if a[key] != b[key]:
                return False
        return True
    except KeyError:
        return False


def compare(old: list, new: list):
    if len(old) != len(new):
        return False
    for (item1, item2) in zip(old, new):
        if not equals(item1, item2):
            return False
    return True


@client.event
async def on_message(message):
    if message.content.lower().startswith("d!"):
        reply = handler.handle_message(message)
        await message.channel.send(reply)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    bot = telegram.Bot(config["TelegramToken"])
    members = {}
    while True:
        for channel_id in handler.channels:
            # get the channels data
            await client.fetch_channel(channel_id)
            channel = client.get_channel(channel_id)

            if channel_id not in members.keys():
                members[channel_id] = []

            # notify if there is a change
            new_members = get_data(channel.members)
            if not compare(members[channel_id], new_members):
                logger.log_var("new_members", new_members)
                logger.log_var("members[channel_id]", members[channel_id])
                notify(members[channel_id], new_members, bot, channel)
            members[channel_id] = get_data(channel.members)


client.run(config["DiscordToken"])
