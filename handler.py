import json
import logger
import validation

_SETTINGS_PATH = "Files/setting.json"
_HELP_PATH = "Files/help.txt"


def read_setting(path=_SETTINGS_PATH):
    with open(path, "r") as reader:
        data = json.loads(reader.read())
        return data["Settings"], data["Channels"]


def read_help(path=_HELP_PATH):
    with open(path, "r") as reader:
        return reader.read()


_help_text = read_help()

_commands = {
    "add": lambda d: add_user(d),
    "update": lambda d: update(d),
    "set": lambda d: set_property(d),
    "remove": lambda d: remove(d),
    "pause": lambda d: deactivate(d),
    "continue": lambda d: activate(d),
    "show": lambda d: show(d),
    "addChannel": lambda d: add_channel(d),
    "removeChannel": lambda d: remove_channel(d),
    "help": lambda d: help_message(d),
    "33": lambda d: "39"  # HaHa ;)
}

_default_values = {
    "Active": True,
    "Join": True,
    "Leave": True,
    "Bots": False,
    "MinMembers": 1,
    "MaxMembers": 9,
    "DetailedMessage": False,
    "ChannelName": False,
    "Channels": []
}

settings, channels = read_setting()


class CommandData:
    def __init__(self, user, command: str, parameters: list, guild):
        self.user = user
        self.command = command
        self.parameters = parameters
        self.guild = guild


def handle_message(msg):
    command, parameters = extract_command(msg.content)
    data = CommandData(msg.author, command, parameters, msg.guild)
    for key in [*_commands]:
        if key.lower() == command.lower():
            return _commands[key](data)
    return f"{command} is not a command, check d!help for help"


def add_user(data: CommandData):
    if data.user.name in settings:
        return "You're already in, use d!show to show your current telegram id or d!update to update it"
    if len(data.parameters) != 1:
        return "I need your telegram id, nothing more, nothing less"
    if not validation.validate_telegram_id(data.parameters[0]):
        return "Can't use this id, are you sure its correct?"
    settings[data.user.name] = dict()
    for key in [*_default_values]:
        settings[data.user.name][key] = _default_values[key]
    settings[data.user.name]["TelegramId"] = int(data.parameters[0])
    save_settings()
    logger.log(f"Added user {data.user.name}")
    return "Your id set to " + data.parameters[0] + " with the default preferences"


def update(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    if not validation.validate_telegram_id(data.parameters[0]):
        return "Can't use this id, are you sure its correct?"
    settings[data.user.name]["TelegramId"] = int(data.parameters[0])
    save_settings()
    return "Updated!"


def set_property(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    try:
        preference = data.parameters[0]
        value = data.parameters[1]

        if preference.lower() not in [x.lower() for x in [*_default_values]] or preference.lower == "active":
            raise KeyError

        for key in [*_default_values]:
            if key.lower() == preference.lower():
                preference = key
                break

        if preference.lower() in ["minmembers", "maxmembers"]:
            value = int(value)
        elif value.lower() not in ["on", "off"]:
            raise ValueError
        else:
            value = value.lower() == "on"

        settings[data.user.name][preference] = value
        save_settings()
    except KeyError:
        return "That's not a preference... use d!help to see the preferences"
    except ValueError:
        return "That's not a value... use d!help to see the preference's values"
    except IndexError:
        return "I need both preference and value, I'm not AI (yet...)"
    return "Updated!"


def remove(data: CommandData):
    if data.user.name not in settings:
        return "Already?! Am I that bad?"
    del settings[data.user.name]
    save_settings()
    logger.log(f"Removed user {data.user.name}")
    return "R.I.P you " + data.user.name


def deactivate(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    settings[data.user.name]["Active"] = False
    save_settings()
    return """
Ok, Boomer...
Use d!continue command to get notifications again
    """


def activate(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    settings[data.user.name]["Active"] = True
    save_settings()
    return "Hell yeah! we're back on track"


def show(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    if len(data.parameters) > 0:
        return str(settings[data.user.name]).replace("{", "").replace("}", "").replace("'", "")

    return f"""
Here's what I know about you {data.user.name}:
Your telegram id is {settings[data.user.name]["TelegramId"]}
Notifications are {"on, good for you" if settings[data.user.name]["Active"] else "off you BOOMER"}
You {"want" if settings[data.user.name]["Join"] else "don't want"} to know when some one enters the channel
You {"want" if settings[data.user.name]["Leave"] else "don't want"} to know when some one leaves the channel
You {"want" if settings[data.user.name]["Bots"] else "don't want"} to know when bot enters or leaves the channel
You'll get a notification when there are between {settings[data.user.name]["MinMembers"]} to {settings[data.user.name]["MaxMembers"]} users talking
You're {"cool" if settings[data.user.name]["DetailedMessage"] else "not cool"} with detailed messages
You {"care" if settings[data.user.name]["ChannelName"] else "don't care"} about the channel info
The channels you track are: {str(settings[data.user.name]["Channels"]).replace("[", "").replace("]", "")}

That's pretty much it 
"""


def add_channel(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    if len(data.parameters) != 1:
        return "I need the channel id, nothing more, nothing less"
    channel_id = int(data.parameters[0])
    name = validation.validate_channel_id(data.guild, channel_id)
    if name == "":
        return "Can't add this channel. Please make sure your in the channel's server and it's the correct id"
    if channel_id not in channels:
        channels.append(channel_id)
    if channel_id not in settings[data.user.name]["Channels"]:
        settings[data.user.name]["Channels"].append(channel_id)
    save_settings()
    logger.log(f"(Channel added by {data.user.name}) total channels in system: {channels}")
    return f"Updated! Added {name} to your track list"


def remove_channel(data: CommandData):
    if data.user.name not in settings:
        return "Add your telegram id first with d!add"
    if len(data.parameters) != 1:
        return "I need the channel id, nothing more, nothing less"
    channel_id = int(data.parameters[0])

    if channel_id in settings[data.user.name]["Channels"]:
        settings[data.user.name]["Channels"].remove(channel_id)

    usage = False
    for value in settings.values():
        if channel_id in value["Channels"]:
            usage = True
            break
    if not usage:
        channels.remove(channel_id)

    logger.log(f"(Channel removed by {data.user.name}) total channels in system: {channels}")
    save_settings()
    return "Updated!"


def help_message(data: CommandData):
    return _help_text


def extract_command(content):
    content = content[2:]  # remove d!
    command = content.split(" ")
    if len(command) == 1:
        return command[0], []
    elif len(command) > 1:
        return command[0], command[1:]
    return "", []


def save_settings(path=_SETTINGS_PATH):
    data = {"Settings": settings, "Channels": channels}
    with open(path, "w") as writer:
        writer.write(json.dumps(data))


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


def get_message(name, channel, old_users, new_users):
    preferences = settings[name]
    if preferences["Active"]:
        msg = ""
        if channel.id not in preferences["Channels"]:
            return ""
        if preferences["MinMembers"] > len(old_users) or preferences["MaxMembers"] < len(new_users):
            return ""
        new_user = find_diff(old_users, new_users)
        if new_users is None:
            return ""
        if new_user["bot"] and not preferences["Bots"]:
            return ""
        if len(old_users) < len(new_users) and preferences["Join"]:
            msg += new_user["name"] + " joined"
        if len(old_users) > len(new_users) and preferences["Leave"]:
            msg += new_user["name"] + " left"
        if preferences["DetailedMessage"]:
            msg += " ( "
            count = 0
            for user in new_users:
                if user["bot"]:
                    continue
                msg += user["name"] + " "
                count += 1
            msg += str(count) + " )"
        if preferences["ChannelName"]:
            msg += " on " + channel.guild.name + "/" + channel.name
        return msg
    return ""
