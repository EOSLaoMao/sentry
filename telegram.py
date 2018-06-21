import requests
from config import TELEGRAM_TOKEN


def get_chats():
    url = 'https://api.telegram.org/bot%s/getUpdates' % TELEGRAM_TOKEN
    res = requests.get(url)
    chats = []
    if res.ok:
        result = res.json()['result']
        for chat in result:
            chat_id = chat['message']['chat']['id']
            chats.append(chat_id)
    return chats

def send_message(message):
    chats = get_chats()
    # print(chats)
    try:
        url = "https://api.telegram.org/bot%s/sendMessage" % TELEGRAM_TOKEN
        print url
        for chat in chats:
            param = {"chat_id": chat, "text": message}
            result = requests.post(url, param, timeout=5.0)
            print("telegram_alarm send result:%s" % result.text)
    except Exception as e:
        print("Get exception:%s" % str(e))
