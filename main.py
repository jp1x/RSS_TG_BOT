import telebot
from telebot import types
import feedparser
import datetime
import time as tm
import sqlite3
import requests
import os
import configparser

def article_is_not_db(article_title, article_date):
    db.execute("SELECT * from myrss WHERE title=? AND date=?", (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

# Добавления поста в БД:
def add_article_to_db(article_title, article_date, article_link):
    db.execute("INSERT INTO myrss VALUES (?,?,?)", (article_title, article_date, article_link))
    db_connection.commit()

def read_article_feed(feed, delay):
    feed = feedparser.parse(feed)
    for article in feed['entries']:
        if article_is_not_db(article['title'], article['published']):
            add_article_to_db(article['title'], article['published'], article['link'])

            data = article.published
            time = datetime.datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
            time_old = config.get('RSS', 'DATETIME')
            time_old = datetime.datetime.strptime(time_old, '%Y-%m-%d  %H:%M:%S%z')

            text = article.title
            print(text)

            link = article.links[0].href
            print(link)

            bot.send_message(CHANNEL, '<a href="' + article['link'] + '">' + article['title'] + '</a>', parse_mode = 'HTML')
            tm.sleep(delay)

config = configparser.ConfigParser()
config.read('cfg.ini')

all_feeds_names = ['1.Лента.ру', '2.Комменрсант.ру', '3.Ведомости - авто', '4.Ведомости - легковые авто', '5.Ведомости - автомобильная промышленность',
'6.Ведомости - технологии', '7.Ведомости - технологии-IT-бизнес', '8.Ведомости - технологии-телекоммуникации', '9.Ведомости - технологии-интернет',
'10.Спорт - футбол', '11.Спорт - хоккей', '12.Спорт - баскетбол', '13.Спорт - теннис', '14.Спорт - формула-1', '15.Медицина', '16.МинОбрНауки']

all_feeds = ['https://lenta.ru/rss', 'https://www.kommersant.ru/RSS/news.xml' , 'https://www.vedomosti.ru/rss/rubric/auto',
'https://www.vedomosti.ru/rss/rubric/auto/cars', 'https://www.vedomosti.ru/rss/rubric/auto/auto_industry', 'https://www.vedomosti.ru/rss/rubric/technology',
'https://www.vedomosti.ru/rss/rubric/technology/it_business', 'https://www.vedomosti.ru/rss/rubric/technology/telecom',
'https://www.vedomosti.ru/rss/rubric/technology/internet', 'https://www.sport-express.ru/services/materials/news/football/se/',
'https://www.sport-express.ru/services/materials/news/hockey/se/', 'https://www.sport-express.ru/services/materials/news/basketball/se/',
'https://www.sport-express.ru/services/materials/news/tennis/se/', 'https://www.sport-express.ru/services/materials/news/formula1/se/',
'http://www.medlinks.ru/news.xm', 'https://minobrnauki.gov.ru/press-center/news/?rss=y']

FEEDS = []
DATETIME = config.get('RSS', 'DATETIME')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'CHANNEL')
bot = telebot.TeleBot(BOT_TOKEN)

# CHANNEL = '@testrss79'
# bot = telebot.TeleBot('5311379840:AAFdI_J5ZuT4v7WV58fdGVN81V1FmhBs9Fk')

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, '<b>Привет! Я бот, умеющий парсить RSS-ленты</b>', parse_mode = 'html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Добавить RSS-ленту')
    item2 = types.KeyboardButton('Показать имеющиеся RSS-ленты')
    item3 = types.KeyboardButton('Выбрать из имеющихся лент')
    item4 = types.KeyboardButton('Удалить все RSS-ленты')
    item5 = types.KeyboardButton('Запустить парсинг лент')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, '<i>Приступаю к работе...</i>', reply_markup=markup, parse_mode = 'html')

#if message.chat.type == 'private':
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.text == 'Добавить RSS-ленту':  
        bot.send_message(message.chat.id, 'Введите ссылку на RSS-ленту: ')
        def add_feed(message):
            FEEDS.append(message.text)
            bot.send_message(message.chat.id, '<i>Добавлено!</i>', parse_mode = 'html')
            print(FEEDS)
        @bot.callback_query_handler(func = lambda call: True)
        def answer(message):
            if message.text != 0:
                add_feed(message)
        bot.register_next_step_handler(message, answer)

    elif message.text == 'Показать имеющиеся RSS-ленты': 
        for name in all_feeds_names:
            bot.send_message(message.chat.id, name)

    elif message.text == 'Выбрать из имеющихся лент': 
        bot.send_message(message.chat.id, 'Введите номер желаемой RSS-ленты')
        @bot.callback_query_handler(func = lambda call: True)
        def answer(number):
            if number.text == '1':
                FEEDS.append(all_feeds[0])
            elif number.text == '2':
                FEEDS.append(all_feeds[1])
            elif number.text == '3':
                FEEDS.append(all_feeds[2])
            elif number.text == '4':
                FEEDS.append(all_feeds[3])
            elif number.text == '5':
                FEEDS.append(all_feeds[4])
            elif number.text == '6':
                FEEDS.append(all_feeds[5])
            elif number.text == '7':
                FEEDS.append(all_feeds[6])
            elif number.text == '8':
                FEEDS.append(all_feeds[7])
            elif number.text == '9':
                FEEDS.append(all_feeds[8])
            elif number.text == '10':
                FEEDS.append(all_feeds[9])
            elif number.text == '11':
                FEEDS.append(all_feeds[10])
            elif number.text == '12':
                FEEDS.append(all_feeds[11])
            elif number.text == '13':
                FEEDS.append(all_feeds[12])
            elif number.text == '14':
                FEEDS.append(all_feeds[13])
            elif number.text == '15':
                FEEDS.append(all_feeds[14])
            elif number.text == '16':
                FEEDS.append(all_feeds[15])

            bot.send_message(message.chat.id, '<i>Добавлено!</i>', parse_mode = 'html')
            print(FEEDS)
    
        bot.register_next_step_handler(message, answer)

    elif message.text == 'Удалить все RSS-ленты':
        FEEDS.clear()
        print(FEEDS)
        bot.send_message(message.chat.id, '<i>Все ленты удалены!</i>', parse_mode = 'html')

    elif message.text == 'Запустить парсинг лент':
        markup=types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1=types.KeyboardButton("3 сек")
        item2=types.KeyboardButton("6 сек")
        item3=types.KeyboardButton("9 сек")
        item4=types.KeyboardButton("15 сек")
        item5=types.KeyboardButton("30 сек")
        item6=types.KeyboardButton("1 мин")
        markup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(message.chat.id,'Выберите задержку', reply_markup = markup)

        def launch_parser(message):
            delaytime = 0
            if message.text == '3 сек':
                delaytime = 3
            elif message.text == '6 сек':
                delaytime = 6
            elif message.text == '9 сек':
                delaytime = 9
            elif message.text == '15 сек':
                delaytime = 15
            elif message.text == '30 сек':
                delaytime = 30
            elif message.text == '1 мин':
                delaytime = 60
            print(delaytime)

            bot.send_message(message.chat.id, '<i>Запускаю...</i>', reply_markup = types.ReplyKeyboardRemove(), parse_mode = 'html')

            item = types.KeyboardButton('Остановить парсинг')
            stop_parse = types.ReplyKeyboardMarkup(resize_keyboard=True)
            stop_parse.add(item)
            bot.send_message(message.chat.id, 'Вы можете в любой момент остановить парсинг', reply_markup = stop_parse)

            for FEED in FEEDS:
                read_article_feed(FEED, delaytime)

        bot.register_next_step_handler(message, launch_parser)

    elif message.text == 'Остановить парсинг':
        bot.send_message(message.chat.id, '<i>Останавливаю...</i>', reply_markup = types.ReplyKeyboardRemove(), parse_mode = 'html')
        db_connection.close()

scriptDir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(scriptDir + '/rss.sqlite', check_same_thread = False)
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS myrss (title TEXT, date TEXT, link TEXT)')

bot.polling(none_stop=True)
