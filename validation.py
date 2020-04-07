import telegram
import telegram.error
import json
import discord
import discord.errors

CONFIG_PATH = "Files/config.json"


def get_config(path=CONFIG_PATH):
    with open(path, "r") as reader:
        config = json.loads(reader.read())
        return config["TelegramToken"], config["DiscordToken"]


TELEGRAM, DISCORD = get_config()


def validate_telegram_id(telegram_id):
    try:
        bot = telegram.Bot(TELEGRAM)
        bot.send_message(chat_id=telegram_id, text="Hello you! You'll get your notifications to hear")
        return True
    except telegram.error.TelegramError:
        return False


def validate_channel_id(guild: discord.Guild, channel_id: int):
    try:
        channel = guild.get_channel(channel_id)
        if channel is None:
            return ""
        return channel.name
    except discord.errors.DiscordException:
        return ""
    except AttributeError:
        return ""
