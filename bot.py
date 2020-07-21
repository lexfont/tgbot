import telebot
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime, date, time
# Google
gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gcredentials = 'telebot-08b97d238c8e.json'
gdocument = 'tbot'

bol = 0

bot = telebot.TeleBot('1330940953:AAFYl2stNUHBlQlO5MuXtT1JEI5hW-pqXN8')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Разместить заказ')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Да', 'Нет')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard1)


link = '';
color = ''
size = ''
number = ''

@bot.message_handler(content_types=['text'])
def start_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if text == "разместить заказ":
        bot.send_message(chat_id, 'Укажите ссылку')
        bot.register_next_step_handler(message, get_link)
def get_link(message):
    global link
    link = message.text
    bot.send_message(message.chat.id, 'Укажите цвет')
    bot.register_next_step_handler(message, get_color)
def get_color(message):
    global color
    color = message.text
    bot.send_message(message.chat.id, 'Укажите размер')
    bot.register_next_step_handler(message, get_size)
def get_size(message):
    global size
    size = message.text
    bot.send_message(message.chat.id, 'Укажите количество')
    bot.register_next_step_handler(message, get_number)
def get_number(message):
    global number
    number = message.text
    bot.register_next_step_handler(message,add_to_gsheet(message='asd', data='213', text='awd'))
def add_to_gsheet(message, data, text):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    wks.append_row(
        [datetime.now().strftime('%d.%m.%Y %H:%M:%S'), link, color, size, number])
    bot.send_message(message.chat,id,'Данные верны?')
    bot.send_message(message.chat, id, link)
    bot.send_message(message.chat, id, color)
    bot.send_message(message.chat, id, size)
    bot.send_message(message.chat, id, number, reply_markup=keyboard2)






bot.polling()