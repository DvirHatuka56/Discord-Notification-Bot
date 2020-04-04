import json

_PATH = "setting.json"


def read_setting(path=_PATH):
    with open(path, "r") as reader:
        data = json.loads(reader.read())
        return data["Settings"], data["Channels"]


_commands = {
    "Add": lambda d: add_user(d),
    "Update": lambda d: update(d),
    "Set": lambda d: set_property(d),
    "Remove": lambda d: remove(d),
    "Pause": lambda d: deactivate(d),
    "Continue": lambda d: activate(d),
    "Show": lambda d: show(d),
    "AddChannel": lambda d: add_channel(d),
    "RemoveChannel": lambda d: remove_channel(d),
    "Help": lambda d: help_message(d)
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
    def __init__(self, user, command, parameters):
        self.user = user
        self.command = command
        self.parameters = parameters


def handle_message(msg):
    command, parameters = extract_command(msg.content)
    data = CommandData(msg.author, command, parameters)
    if command in [*_commands]:
        reply = _commands[command](data)
    else:
        reply = help_message(data)
    return reply


def add_user(data):
    if data.user.name in settings:
        return "You're already in, use DNB!Show to show your current telegram id or DNB!Update to update it"
    if len(data.parameters) != 1:
        return "I need your telegram id, nothing more, nothing less"
    settings[data.user.name] = dict()
    for key in [*_default_values]:
        settings[data.user.name][key] = _default_values[key]
    settings[data.user.name]["TelegramId"] = int(data.parameters[0])
    save_settings()
    return "Your id set to " + data.parameters[0] + " with the default preferences"


def update(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    settings[data.user.name]["TelegramId"] = int(data.parameters[0])
    save_settings()
    return "Updated!"


def set_property(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    try:
        preference = data.parameters[0]
        value = data.parameters[1]

        if preference not in [*_default_values] or preference == "Active":
            raise KeyError

        if preference in ["MinMembers", "MaxMembers"]:
            value = int(value)
        elif value not in ["On", "Off"]:
            raise ValueError
        else:
            value = value == "On"

        settings[data.user.name][preference] = value
        save_settings()
    except KeyError:
        return "That's not a preference... use DNB!Help to see the preferences"
    except ValueError:
        return "That's not a value... use DNB!Help to see the preference's values"
    except IndexError:
        return "I need both preference and value, I'm not AI (yet...)"
    return "Updated!"


def remove(data):
    if data.user.name not in settings:
        return "Already?! Am I that bad?"
    del settings[data.user.name]
    save_settings()
    return "R.I.P you " + data.user.name


def deactivate(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    settings[data.user.name]["Active"] = False
    save_settings()
    return """
Ok, Boomer...
Use DNB!Continue command to get notifications again
    """


def activate(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    settings[data.user.name]["Active"] = True
    save_settings()
    return "Hell yeah! we're back on track"


def show(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    if len(data.parameters) > 0:
        return str(settings[data.user.name]).replace("{", "").replace("}", "").replace("'", "")

    # TODO: add additional data
    return f"""
Here's what I know about you {data.user.name}:
Your telegram id is {settings[data.user.name]["TelegramId"]}
Notifications are {"on, good for you" if settings[data.user.name]["Active"] else "off you BOOMER"}
You {"want" if settings[data.user.name]["Join"] else "don't want"} to know when some one enters the channel
You {"want" if settings[data.user.name]["Leave"] else "don't want"} to know when some one leaves the channel
You {"want" if settings[data.user.name]["Bots"] else "don't want"} to know when bot enters or leaves the channel
You'll get a notification when there are between {settings[data.user.name]["MinMembers"]} to {settings[data.user.name]["MaxMembers"]} users talking
You're {"cool" if settings[data.user.name]["DetailedMessage"] else "not cool"} with detailed messages

That's pretty much it 
"""


def add_channel(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    if len(data.parameters) != 1:
        return "I need the channel id, nothing more, nothing less"
    channel_id = int(data.parameters[0])
    if channel_id not in channels:
        channels.append(channel_id)
    if channel_id not in settings[data.user.name]["Channels"]:
        settings[data.user.name]["Channels"].append(channel_id)
    save_settings()
    return "Updated!"


def remove_channel(data):
    if data.user.name not in settings:
        return "Add your telegram id first with DNB!Add"
    if len(data.parameters) != 1:
        return "I need the channel id, nothing more, nothing less"
    channel_id = int(data.parameters[0])
    # TODO: remove from global channels if no one use the channel
    if channel_id in settings[data.user.name]["Channels"]:
        settings[data.user.name]["Channels"].remove(channel_id)
    save_settings()
    return "Updated!"


def help_message(data):
    msg = ""
    command = data.command
    if command not in _commands.keys():
        msg += command + " is not a command."

    # TODO: add info on the remove channel command
    msg += """
The available commands are:
DNB!Add TELEGRAM_ID - add your telegram id
DNB!Update TELEGRAM_ID - update your telegram id
DNB!AddChannel CHANNEL_ID - add channel that you want to get notifications on
DNB!Set Preference Value - set a notification preference to a certain value
DNB!Remove - remove yourself from the service
DNB!Pause - pause the service
DNB!Continue - continue the service
DNB!Help - help info
DNB!Show - show your preferences 

Preferences:
Join (On / Off) - get notification whenever user connects  
Leave (On / Off) - get notification whenever user disconnects
Bots (On / Off) - get notification whenever bots connects / disconnects
DetailedMessage (On / Off) - get notification with the names of the users and the number of users connected
ChannelName (On / Off) - get notification with the channel's name
MinConnected (number) - get notification when there are more than a certain numbers of users connected
MaxConnected (number) - DONT get notification when there are more than a certain numbers of users connected

Dvir Hatuka - 2020, https://github.com/DvirHatuka56/Discord-Notification-Bot
    """

    return msg


def extract_command(content):
    content = content[4:]  # remove DNB!
    command = content.split(" ")
    if len(command) == 1:
        return command[0], []
    elif len(command) > 1:
        return command[0], command[1:]
    return "", []


def save_settings(path=_PATH):
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
        if new_user.bot and preferences["Bots"]:
            return ""
        if len(old_users) < len(new_users) and preferences["Join"]:
            msg += new_user.name + " joined"
        if len(old_users) > len(new_users) and preferences["Leave"]:
            msg += new_user.name + " left"
        if preferences["DetailedMessage"]:
            msg += " ( "
            for user in new_users:
                msg += user.name
            msg += str(len(new_users)) + " )"
        if preferences["ChannelName"]:
            msg += " on " + channel.guild.name + "/" + channel.name
        return msg
    return ""
