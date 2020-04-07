import telegram
import telegram.error
import json


def get_config(path="config.json"):
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