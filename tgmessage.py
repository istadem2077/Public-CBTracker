import requests


def telegram_sendmessage(bot_chatID, bot_message):

    bot_token = "6***"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + f"{bot_chatID}" + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()

