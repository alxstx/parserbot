import telebot
import time
from telebot import types
import urllib.request as urllib2
from PIL import Image
from bs4 import BeautifulSoup
import requests
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context  #
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
info_txt = '''
Это телеграм бот, который вам каждый час присылает новую
акцию с Wildberries. В начале вы можете выбрать вещи, о которых вам будет
присылаться информация, послав ее боту. Но  вы можете позже изменить выбор 
через команду /change
'''
info_txt2 = '''
Выберите товары:
'''
super_dict = {'Аксессуары': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/aksessuary',
              'Аксессуары для волос': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/aksessuary-dlya-volos',
              'Аксессуары для малышей': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/aksessuary-dlya-malyshey',
              'Аксессуары для Обуви': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/aksessuary-dlya-obuvi',
              'Белье': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/bele',
              'Белье для малышей': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/bele-dlya-malyshey',
              'Бижутерия': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/bizhuteriya',
              'Головные уборы': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/golovnye-ubory',
              'Для праздника': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/dlya-prazdnika',
              'Обувь': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/obuv',
              'Одежда': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/odezhda',
              'Одежда для малышей': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/odezhda-dlya-malyshey',
              'Спортивная Обувь': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/sportivnaya-obuv',
              'Спортивная Одежда': 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary/sportivnaya-odezhda'}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
bot = telebot.TeleBot('your token')  # новый токен
hello = True
numbers = []
chosen_things = []
whole_info_list = []
filtered_list = []
chosen_things2 = []
counters = []
stopping = []


def get_html(url, params):
    r = requests.get(url, headers=headers, params=params)
    return r


def get_content(html, ):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='dtList-inner')
    things = []
    for item in items:
        try:
            things.append({'title': item.find('div', 'dtlist-inner-brand-name').get_text(strip=True),
                           'price': item.find('ins', 'lower-price').get_text(strip=True).replace(u'\xa0', u' '),
                           'photo': item.find('div', 'l_class').find_next('img').get('src'),
                           'link': 'https://www.wildberries.ru' + item.find('a',
                                                                            'ref_goods_n_p j-open-full-product-card').get(
                               'href')})
        except AttributeError:
            pass
    return things


def parse(chosen_things):
    url1 = 'https://www.wildberries.ru/promotions/final-rasprodazh-odezhda-obuv-aksessuary?bid=9376696e-6e57-44cd-bae7-e6f9c4a1e88a'
    html = get_html(url1, params=None)
    if html.status_code == 200:
        things = []
        for chose in chosen_things:
            print('Parsing...')
            html = get_html(super_dict[chose], params=None)
            things.extend(get_content(html.text))
        return things
    else:
        print(html)
        things = []
        return things


def filter_list(items):
    for i in items:
        if i not in filtered_list:
            filtered_list.append(i)
        else:
            pass


def sends(message):
    if filtered_list != []:
        for info in filtered_list:
            photo = Image.open(urllib2.urlopen('https:' + info['photo'].strip()))
            if info['photo'].strip() != '//static.wbstatic.net/i/blank.gif':
                bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, info['title'])
            bot.send_message(message.chat.id, info['price'])
            bot.send_message(message.chat.id, info['link'])
            time.sleep(3600)
            if bool(stopping):
                filtered_list.clear()
                break
    else:
        bot.send_message(message.chat.id, 'Произлошла ошибка, напишите автору этого бота: @alex_stepp')


def recv_parse_info(message):
    counters.append('1')
    info_list = parse(chosen_things)
    filter_list(info_list)
    sends(message)


def choice_made(message, bot):
    time.sleep(20)
    mark2 = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
    btn2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
    mark2.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вы сделали выбор?', reply_markup=mark2)


@bot.message_handler(commands=['start', 'change'])
def start_text(message):
    if bool(counters):
        stopping.append('stop')
    mark = types.InlineKeyboardMarkup(row_width=2)
    a = 0
    chosen_things.clear()
    numbers.clear()
    whole_info_list.clear()
    for i in super_dict.keys():
        if hello:
            text = i
        else:
            text = i + '✅'
        btn = types.InlineKeyboardButton(text=text, callback_data=str(a))
        mark.add(btn)
        a += 1
    if message.text == '/start':
        bot.send_message(message.chat.id, info_txt)
    time.sleep(3)
    bot.send_message(message.chat.id, info_txt2, reply_markup=mark)
    time.sleep(3)
    choice_made(message, bot)


@bot.message_handler(content_types=['text'])
def hand_func(message):
    sticker = open('stickermeme.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)


@bot.callback_query_handler(func=lambda mess: True)
def act2(call):
    a = 0
    j_list = [j for j in range(0, 30)]
    try:
        call_data = int(call.data)
    except:
        call_data = str(call.data)
    if call_data in j_list:
        chosen_things.clear()
        numbers.append(j_list[int(call.data)])
        hello = False
        mark = types.InlineKeyboardMarkup(row_width=2)
        for i in super_dict.keys():
            if not hello and a not in numbers:
                text = i
            else:
                text = i + '✅'
            btn = types.InlineKeyboardButton(text=text, callback_data=str(a))
            if '✅' in text:
                chosen_things.append(text[0:text.index('✅')])
            mark.add(btn)
            a += 1
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=mark)
        except:
            pass
    if call_data == 'yes':
        stopping.clear()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        time.sleep(3)
        recv_parse_info(call.message)
    if call_data == 'no':
        time.sleep(10)
        choice_made(call.message, bot)


bot.polling(none_stop=True)
