# pip isntall openai
import openai
import os
import json
from base64 import b64decode
import telebot
from time import sleep

mes = ''
file_name = ''

with open('API_GPT.txt', 'r', encoding='utf-8-sig') as fp:
    API_KEY_GPT = fp.read().rstrip()

with open('API_TLG.txt', 'r', encoding='utf-8-sig') as fp:
    API_KEY_TLG = fp.read().rstrip()

# prompt = input('The prompt: ')
# openai.api_key = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY_TLG)
openai.api_key = API_KEY_GPT

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! ' + str(m.from_user.username) + ' Я на связи. Какую картинку нарисуем? )')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    mes = message.text
    ChatId = message.chat.id

    response = openai.Image.create(
        prompt=mes,
        n=1,
        size='512x512',
        response_format='b64_json'
    )

    with open('data.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    image_data = b64decode(response['data'][0]['b64_json'])
    file_name = '_'.join(mes.split(' '))

    with open(f'{file_name}.png', 'wb') as file:
        file.write(image_data)

    #sleep(30)

    bot.send_photo(ChatId, open(f'{file_name}.png', 'rb'))

bot.polling(none_stop=True, interval=0)
