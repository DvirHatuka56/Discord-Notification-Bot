# Discord Notification Bot
Discord Notification Bot - Every time there are users talking in a certain channel, a message about it will be sent to you

# Create config file

create file in the project directory named config.json

    {
      "DiscordToken": "DISCORD_TOKEN",
      "TelegramToken": "TELEGRAM_TOKEN",
      "UserId": [USER_ID1, USER_ID2],
      "ServerId": SERVER_ID,
      "ChannelId": CHANNEL_ID
    }
   
#### Setting up the tokens and ids

    DISCORD_TOKEN
look here how to get the token \
https://www.writebots.com/discord-bot-token/ \
Enter this value as a string


    TELEGRAM_TOKEN
look here how to get the token \
https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token \
Enter this value as a string


    USER_ID
look here how to get it \
https://support.bigone.com/hc/en-us/articles/360008014894-How-to-get-the-Telegram-user-ID- \
Enter this value as an int (you can add more than one, its a list)

    CHANNEL_ID SERVER_ID
look here how to get those \
https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID- \
Enter those values as ints
