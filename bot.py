import discord
import telegram
import json
import handler
import logger


def get_config(path="config.json"):
    with open(path, "r") as reader:
        return json.loads(reader.read())


client = discord.Client()
config = get_config()


def notify(members, new_members, bot, channel):
    for user in [*handler.settings]:
        message = handler.get_message(user, channel, members, new_members)
        if message == "":
            continue
        logger.log(f"(to {user}) {message}d!removeChannel")
        bot.send_message(chat_id=handler.settings[user]["TelegramId"], text=message)


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
        # get the channels data
        for channel_id in handler.channels:
            await client.fetch_channel(channel_id)
            channel = client.get_channel(channel_id)

            if channel_id not in members.keys():
                members[channel_id] = []

            # notify if there is more than one member
            if channel.members != members[channel_id]:
                notify(members[channel_id], channel.members, bot, channel)
            members[channel_id] = channel.members


client.run(config["DiscordToken"])
