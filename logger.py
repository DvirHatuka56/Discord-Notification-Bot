import datetime

PATH = "Files/log.txt"


def log(text):
    with open(PATH, "a", encoding='UTF-8') as writer:
        now = datetime.datetime.now()
        date = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}"
        writer.write(f"{date}: {text}\n")
