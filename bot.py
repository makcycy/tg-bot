import telegram
from time import sleep
import new_ipo

f = open('bot_token', 'r')
token = f.readline()
Bot = telegram.Bot(token)
last_msg_id = 0

def getText(Update):
    return Update["message"]['text']

def getMsgId(Update):
    return Update['update_id']

def getChatId(Update):
    return Update['message']['chat']['id']

def getUserId(Update):
    return Update['message']['from_user']['id']

def messgeHandler(Update):
    global last_msg_id
    text = getText(Update)
    msg_id = getMsgId(Update)
    user_id = getUserId(Update)
    last_msg_id = msg_id
    if text =='/new_ipo':
        Bot.sendMessage(user_id, new_ipo.getmessage())

    print(user_id, msg_id, text)
    return None

def main():
    global last_msg_id
    updates = Bot.getUpdates()
    if len(updates) > 0:
        last_msg_id = updates[-1]["update_id"]
    while True:
        updates = Bot.getUpdates(offset = last_msg_id)
        updates = [update for update in updates if update["update_id"]>last_msg_id]
        for update in updates:
            messgeHandler(update)
        sleep(0.5)


if __name__ == '__main__':
    main()