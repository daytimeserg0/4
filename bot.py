import telebot
from telebot import types
import psycopg2
import datetime

dates_first_week = ['2023-02-27', '2023-02-28', '2023-03-01', '2023-03-02', '2023-03-03', '2023-03-04', '2023-03-05', '2023-03-13', '2023-03-14',
                    '2023-03-15', '2023-03-16', '2023-03-17', '2023-03-18', '2023-03-19', '2023-03-27', '2023-03-28', '2023-03-29', '2023-03-30',
                    '2023-03-31', '2023-04-01', '2023-04-02', '2023-04-10', '2023-04-11', '2023-04-12', '2023-04-13', '2023-04-14', '2023-04-15',
                    '2023-04-16', '2023-04-24', '2023-04-25', '2023-04-26', '2023-04-27', '2023-04-28', '2023-04-29', '2023-04-30', '2023-05-08',
                    '2023-05-09', '2023-05-10', '2023-05-11', '2023-05-12', '2023-05-13', '2023-05-14', '2023-05-22', '2023-05-23', '2023-05-24',
                    '2023-05-25', '2023-05-26', '2023-05-27', '2023-05-28', '2023-06-05', '2023-06-06', '2023-06-07', '2023-06-08', '2023-06-09',
                    '2023-06-10', '2023-06-11', '2023-06-19', '2023-06-20', '2023-06-21', '2023-06-22', '2023-06-23', '2023-06-24', '2023-06-25']


conn = psycopg2.connect(dbname='schedule', user='postgres', password="A123a123s", host="localhost", port="5432")

cursor = conn.cursor()
cursor.execute("SELECT first_week.day, first_week.time, subject.name, teacher.name,"
               " first_week.room FROM first_week JOIN subject ON first_week.subject = subject.name JOIN teacher ON subject.name = teacher.subject;")
f = (list(cursor.fetchall()))
cursor.execute('SELECT second_week.day, second_week.time, subject.name, teacher.name,'
               ' second_week.room FROM second_week JOIN subject ON second_week.subject = subject.name JOIN teacher ON subject.name = teacher.subject;')
s = (list(cursor.fetchall()))

token = '5916026021:AAHRpg0iySLVRJ9yqm4KgDRy6iF-dJZuZnw'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
def help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.row("/help")
    bot.send_message(message.chat.id, 'Здравствуйте, я бот с расписанием группы БВТ2203\n'
                                      'Список моих возможностей:\n\n'
                                      '/help , /start - Вывести это сообщение повторно\n\n'
                                      '/1week - Получить расписание на нечетную неделю\n\n'
                                      '/2week - Получить расписание на четную неделю\n\n'
                                      '/days - Получить расписание на конкретный день\n\n'
                                      '/current_week - Узнать текущую неделю\n\n'
                                      '/mtuci Получить ссылку на официальный сайт МТУСИ'
                     , reply_markup=keyboard)

@bot.message_handler(commands=['current_week'])
def current_week(message):
    today = datetime.date.today()
    if str(today) in dates_first_week:
        bot.send_message(message.chat.id, 'Текущая неделя - нечетная')
    else:
        bot.send_message(message.chat.id, 'Текущая неделя - четная')


@bot.message_handler(commands=['days'])
def week(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_first = types.InlineKeyboardButton(text = 'Нечетная неделя', callback_data = 'first')
    item_second = types.InlineKeyboardButton(text = 'Четная неделя', callback_data = 'second')

    markup_inline.add(item_first, item_second)
    bot.send_message(message.chat.id, 'Выберите нужную неделю', reply_markup = markup_inline)


@bot.callback_query_handler(func = lambda call: True)
def day(call):
    if call.data == 'first':
        markup_inline2 = types.InlineKeyboardMarkup()
        item_1mon = types.InlineKeyboardButton(text='Понедельник', callback_data='1mon')
        item_1tue = types.InlineKeyboardButton(text='Вторник', callback_data='1tue')
        item_1wed = types.InlineKeyboardButton(text='Среда', callback_data='1wed')
        item_1thu = types.InlineKeyboardButton(text='Четверг', callback_data='1thu')
        item_1fri = types.InlineKeyboardButton(text='Пятница', callback_data='1fri')
        item_1sat = types.InlineKeyboardButton(text='Суббота', callback_data='1sat')
        markup_inline2.add(item_1mon, item_1tue, item_1wed, item_1thu, item_1fri, item_1sat)
        bot.send_message(call.message.chat.id, 'На какой день недели хотите получить расписание?', reply_markup = markup_inline2)
    elif call.data == 'second':
        markup_inline3 = types.InlineKeyboardMarkup()
        item_2mon = types.InlineKeyboardButton(text='Понедельник', callback_data='2mon')
        item_2tue = types.InlineKeyboardButton(text='Вторник', callback_data='2tue')
        item_2wed = types.InlineKeyboardButton(text='Среда', callback_data='2wed')
        item_2thu = types.InlineKeyboardButton(text='Четверг', callback_data='2thu')
        item_2fri = types.InlineKeyboardButton(text='Пятница', callback_data='2fri')
        item_2sat = types.InlineKeyboardButton(text='Суббота', callback_data='2sat')
        markup_inline3.add(item_2mon, item_2tue, item_2wed, item_2thu, item_2fri, item_2sat)
        bot.send_message(call.message.chat.id, 'На какой день недели хотите получить расписание?', reply_markup = markup_inline3)
    elif call.data == '1mon':bot.send_message (call.message.chat.id, f'Понедельник\n\n'
                                                                     f'{f[0][1]}: {f[0][2]} | {f[0][3]} | {f[0][4]}\n\n'
                                                                     f'{f[1][1]}: {f[1][2]} | {f[1][3]} | {f[1][4]}\n\n'
                                                                     f'{f[2][1]}: {f[2][2]} | {f[2][3]} | {f[2][4]}\n\n'
                                                                     f'{f[3][1]}: {f[3][2]} | {f[3][3]} | {f[3][4]}\n\n'
                                                                     f'{f[4][1]}: {f[4][2]} | {f[4][3]} | {f[4][4]}')
    elif call.data == '1tue':bot.send_message (call.message.chat.id, f'Вторник\n\n'
                                                                     f'{f[5][1]}: {f[5][2]} | {f[5][3]} | {f[5][4]}\n\n'
                                                                     f'{f[6][1]}: {f[6][2]} | {f[6][3]} | {f[6][4]}\n\n'
                                                                     f'{f[7][1]}: {f[7][2]} | {f[7][3]} | {f[7][4]}\n\n'
                                                                     f'{f[8][1]}: {f[8][2]} | {f[8][3]} | {f[8][4]}\n\n'
                                                                     f'{f[9][1]}: {f[9][2]} | {f[9][3]} | {f[9][4]}')
    elif call.data == '1wed':bot.send_message (call.message.chat.id, f'Среда\n\n'
                                                                     f'{f[10][1]}: {f[10][2]} | {f[10][3]} | {f[10][4]}\n\n'
                                                                     f'{f[11][1]}: {f[11][2]} | {f[11][3]} | {f[11][4]}\n\n'
                                                                     f'{f[12][1]}: {f[12][2]} | {f[12][3]} | {f[12][4]}\n\n'
                                                                     f'{f[13][1]}: {f[13][2]} | {f[13][3]} | {f[13][4]}\n\n'
                                                                     f'{f[14][1]}: {f[14][2]} | {f[14][3]} | {f[14][4]}')
    elif call.data == '1thu':bot.send_message (call.message.chat.id, f'Четверг\n\n'
                                                                     f'{f[15][1]}: {f[15][2]} | {f[15][3]} | {f[15][4]}\n\n'
                                                                     f'{f[16][1]}: {f[16][2]} | {f[16][3]} | {f[16][4]}\n\n'
                                                                     f'{f[17][1]}: {f[17][2]} | {f[17][3]} | {f[17][4]}\n\n'
                                                                     f'{f[18][1]}: {f[18][2]} | {f[18][3]} | {f[18][4]}\n\n'
                                                                     f'{f[19][1]}: {f[19][2]} | {f[19][3]} | {f[19][4]}')
    elif call.data == '1fri':bot.send_message (call.message.chat.id, f'Пятница\n\n'
                                                                     f'{f[20][1]}: {f[20][2]} | {f[20][3]} | {f[20][4]}\n\n'
                                                                     f'{f[21][1]}: {f[21][2]} | {f[21][3]} | {f[21][4]}\n\n'
                                                                     f'{f[22][1]}: {f[22][2]} | {f[22][3]} | {f[22][4]}\n\n'
                                                                     f'{f[23][1]}: {f[23][2]} | {f[23][3]} | {f[23][4]}\n\n'
                                                                     f'{f[24][1]}: {f[24][2]} | {f[24][3]} | {f[24][4]}')
    elif call.data == '1sat':bot.send_message (call.message.chat.id, f'Суббота\n\n'
                                                                     f'{f[25][1]}: {f[25][2]} | {f[25][3]} | {f[25][4]}\n\n'
                                                                     f'{f[26][1]}: {f[26][2]} | {f[26][3]} | {f[26][4]}\n\n'
                                                                     f'{f[27][1]}: {f[27][2]} | {f[27][3]} | {f[27][4]}\n\n'
                                                                     f'{f[28][1]}: {f[28][2]} | {f[28][3]} | {f[28][4]}\n\n'
                                                                     f'{f[29][1]}: {f[29][2]} | {f[29][3]} | {f[29][4]}')
    elif call.data == '2mon':bot.send_message (call.message.chat.id, f'Понедельник\n\n'
                                                                     f'{s[0][1]}: {s[0][2]} | {s[0][3]} | {s[0][4]}\n\n'
                                                                     f'{s[1][1]}: {s[1][2]} | {s[1][3]} | {s[1][4]}\n\n'
                                                                     f'{s[2][1]}: {s[2][2]} | {s[2][3]} | {s[2][4]}\n\n'
                                                                     f'{s[3][1]}: {s[3][2]} | {s[3][3]} | {s[3][4]}\n\n'
                                                                     f'{s[4][1]}: {s[4][2]} | {s[4][3]} | {s[4][4]}')
    elif call.data == '2tue':bot.send_message (call.message.chat.id, f'Вторник\n\n'
                                                                     f'{s[5][1]}: {s[5][2]} | {s[5][3]} | {s[5][4]}\n\n'
                                                                     f'{s[6][1]}: {s[6][2]} | {s[6][3]} | {s[6][4]}\n\n'
                                                                     f'{s[7][1]}: {s[7][2]} | {s[7][3]} | {s[7][4]}\n\n'
                                                                     f'{s[8][1]}: {s[8][2]} | {s[8][3]} | {s[8][4]}\n\n'
                                                                     f'{s[9][1]}: {s[9][2]} | {s[9][3]} | {s[9][4]}')
    elif call.data == '2wed':bot.send_message (call.message.chat.id, f'Среда\n\n'
                                                                     f'{s[10][1]}: {s[10][2]} | {s[10][3]} | {s[10][4]}\n\n'
                                                                     f'{s[11][1]}: {s[11][2]} | {s[11][3]} | {s[11][4]}\n\n'
                                                                     f'{s[12][1]}: {s[12][2]} | {s[12][3]} | {s[12][4]}\n\n'
                                                                     f'{s[13][1]}: {s[13][2]} | {s[13][3]} | {s[13][4]}\n\n'
                                                                     f'{s[14][1]}: {s[14][2]} | {s[14][3]} | {s[14][4]}')
    elif call.data == '2thu':bot.send_message (call.message.chat.id, f'Четверг\n\n'
                                                                     f'{s[15][1]}: {s[15][2]} | {s[15][3]} | {s[15][4]}\n\n'
                                                                     f'{s[16][1]}: {s[16][2]} | {s[16][3]} | {s[16][4]}\n\n'
                                                                     f'{s[17][1]}: {s[17][2]} | {s[17][3]} | {s[17][4]}\n\n'
                                                                     f'{s[18][1]}: {s[18][2]} | {s[18][3]} | {s[18][4]}\n\n'
                                                                     f'{s[19][1]}: {s[19][2]} | {s[19][3]} | {s[19][4]}')
    elif call.data == '2fri':bot.send_message (call.message.chat.id, f'Пятница\n\n'
                                                                     f'{s[20][1]}: {s[20][2]} | {s[20][3]} | {s[20][4]}\n\n'
                                                                     f'{s[21][1]}: {s[21][2]} | {s[21][3]} | {s[21][4]}\n\n'
                                                                     f'{s[22][1]}: {s[22][2]} | {s[22][3]} | {s[22][4]}\n\n'
                                                                     f'{s[23][1]}: {s[23][2]} | {s[23][3]} | {s[23][4]}\n\n'
                                                                     f'{s[24][1]}: {s[24][2]} | {s[24][3]} | {s[24][4]}')
    elif call.data == '2sat':bot.send_message (call.message.chat.id, f'Суббота\n\n'
                                                                     f'{s[25][1]}: {s[25][2]} | {s[25][3]} | {s[25][4]}\n\n'
                                                                     f'{s[26][1]}: {s[26][2]} | {s[26][3]} | {s[26][4]}\n\n'
                                                                     f'{s[27][1]}: {s[27][2]} | {s[27][3]} | {s[27][4]}\n\n'
                                                                     f'{s[28][1]}: {s[28][2]} | {s[28][3]} | {s[28][4]}\n\n'
                                                                     f'{s[29][1]}: {s[29][2]} | {s[29][3]} | {s[29][4]}')


@bot.message_handler(commands=['1week'])
def start_message(message):
    bot.send_message(message.chat.id, 'Нечетная неделя\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nПонедельник\n\n'
                     f'{f[0][1]}: {f[0][2]} | {f[0][3]} | {f[0][4]}\n\n'
                     f'{f[1][1]}: {f[1][2]} | {f[1][3]} | {f[1][4]}\n\n'
                     f'{f[2][1]}: {f[2][2]} | {f[2][3]} | {f[2][4]}\n\n'
                     f'{f[3][1]}: {f[3][2]} | {f[3][3]} | {f[3][4]}\n\n'
                     f'{f[4][1]}: {f[4][2]} | {f[4][3]} | {f[4][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nВторник\n\n'
                     
                     f'{f[5][1]}: {f[5][2]} | {f[5][3]} | {f[5][4]}\n\n'
                     f'{f[6][1]}: {f[6][2]} | {f[6][3]} | {f[6][4]}\n\n'
                     f'{f[7][1]}: {f[7][2]} | {f[7][3]} | {f[7][4]}\n\n'
                     f'{f[8][1]}: {f[8][2]} | {f[8][3]} | {f[8][4]}\n\n'
                     f'{f[9][1]}: {f[9][2]} | {f[9][3]} | {f[9][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nСреда\n\n'
                     
                     f'{f[10][1]}: {f[10][2]} | {f[10][3]} | {f[10][4]}\n\n'
                     f'{f[11][1]}: {f[11][2]} | {f[11][3]} | {f[11][4]}\n\n'
                     f'{f[12][1]}: {f[12][2]} | {f[12][3]} | {f[12][4]}\n\n'
                     f'{f[13][1]}: {f[13][2]} | {f[13][3]} | {f[13][4]}\n\n'
                     f'{f[14][1]}: {f[14][2]} | {f[14][3]} | {f[14][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nЧетверг\n\n'
                     
                     f'{f[15][1]}: {f[15][2]} | {f[15][3]} | {f[15][4]}\n\n'
                     f'{f[16][1]}: {f[16][2]} | {f[16][3]} | {f[16][4]}\n\n'
                     f'{f[17][1]}: {f[17][2]} | {f[17][3]} | {f[17][4]}\n\n'
                     f'{f[18][1]}: {f[18][2]} | {f[18][3]} | {f[18][4]}\n\n'
                     f'{f[19][1]}: {f[19][2]} | {f[19][3]} | {f[19][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nПятница\n\n'
                     
                     f'{f[20][1]}: {f[20][2]} | {f[20][3]} | {f[20][4]}\n\n'
                     f'{f[21][1]}: {f[21][2]} | {f[21][3]} | {f[21][4]}\n\n'
                     f'{f[22][1]}: {f[22][2]} | {f[22][3]} | {f[22][4]}\n\n'
                     f'{f[23][1]}: {f[23][2]} | {f[23][3]} | {f[23][4]}\n\n'
                     f'{f[24][1]}: {f[24][2]} | {f[24][3]} | {f[24][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nСуббота\n\n'

                     f'{f[25][1]}: {f[25][2]} | {f[25][3]} | {f[25][4]}\n\n'
                     f'{f[26][1]}: {f[26][2]} | {f[26][3]} | {f[26][4]}\n\n'
                     f'{f[27][1]}: {f[27][2]} | {f[27][3]} | {f[27][4]}\n\n'
                     f'{f[28][1]}: {f[28][2]} | {f[28][3]} | {f[28][4]}\n\n'
                     f'{f[29][1]}: {f[29][2]} | {f[29][3]} | {f[29][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')


@bot.message_handler(commands=['2week'])
def start_message(message):
    bot.send_message(message.chat.id, 'Четная неделя\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nПонедельник\n\n'
                     f'{s[0][1]}: {s[0][2]} | {s[0][3]} | {s[0][4]}\n\n'
                     f'{s[1][1]}: {s[1][2]} | {s[1][3]} | {s[1][4]}\n\n'
                     f'{s[2][1]}: {s[2][2]} | {s[2][3]} | {s[2][4]}\n\n'
                     f'{s[3][1]}: {s[3][2]} | {s[3][3]} | {s[3][4]}\n\n'
                     f'{s[4][1]}: {s[4][2]} | {s[4][3]} | {s[4][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nВторник\n\n'
                     
                     f'{s[5][1]}: {s[5][2]} | {s[5][3]} | {s[5][4]}\n\n'
                     f'{s[6][1]}: {s[6][2]} | {s[6][3]} | {s[6][4]}\n\n'
                     f'{s[7][1]}: {s[7][2]} | {s[7][3]} | {s[7][4]}\n\n'
                     f'{s[8][1]}: {s[8][2]} | {s[8][3]} | {s[8][4]}\n\n'
                     f'{s[9][1]}: {s[9][2]} | {s[9][3]} | {s[9][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nСреда\n\n'
                     
                     f'{s[10][1]}: {s[10][2]} | {s[10][3]} | {s[10][4]}\n\n'
                     f'{s[11][1]}: {s[11][2]} | {s[11][3]} | {s[11][4]}\n\n'
                     f'{s[12][1]}: {s[12][2]} | {s[12][3]} | {s[12][4]}\n\n'
                     f'{s[13][1]}: {s[13][2]} | {s[13][3]} | {s[13][4]}\n\n'
                     f'{s[14][1]}: {s[14][2]} | {s[14][3]} | {s[14][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nЧетверг\n\n'
                     
                     f'{s[15][1]}: {s[15][2]} | {s[15][3]} | {s[15][4]}\n\n'
                     f'{s[16][1]}: {s[16][2]} | {s[16][3]} | {s[16][4]}\n\n'
                     f'{s[17][1]}: {s[17][2]} | {s[17][3]} | {s[17][4]}\n\n'
                     f'{s[18][1]}: {s[18][2]} | {s[18][3]} | {s[18][4]}\n\n'
                     f'{s[19][1]}: {s[19][2]} | {s[19][3]} | {s[19][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nПятница\n\n'
                     
                     f'{s[20][1]}: {s[20][2]} | {s[20][3]} | {s[20][4]}\n\n'
                     f'{s[21][1]}: {s[21][2]} | {s[21][3]} | {s[21][4]}\n\n'
                     f'{s[22][1]}: {s[22][2]} | {s[22][3]} | {s[22][4]}\n\n'
                     f'{s[23][1]}: {s[23][2]} | {s[23][3]} | {s[23][4]}\n\n'
                     f'{s[24][1]}: {s[24][2]} | {s[24][3]} | {s[24][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nСуббота\n\n'

                     f'{s[25][1]}: {s[25][2]} | {s[25][3]} | {s[25][4]}\n\n'
                     f'{s[26][1]}: {s[26][2]} | {s[26][3]} | {s[26][4]}\n\n'
                     f'{s[27][1]}: {s[27][2]} | {s[27][3]} | {s[27][4]}\n\n'
                     f'{s[28][1]}: {s[28][2]} | {s[28][3]} | {s[28][4]}\n\n'
                     f'{s[29][1]}: {s[29][2]} | {s[29][3]} | {s[29][4]}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')


@bot.message_handler(commands=['mtuci'])
def answer(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ - https://mtuci.ru/')


@bot.message_handler(content_types = ['text'])
def send_message(message):
    if message.text.lower() == 'Привет':
        bot.send_message(message.chat.id, 'Здравсвтуй, я бот с расписанием группы БВТ2203! Нажмите /help чтобы узнать мои возможности.')
    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понял. Нажмите /help чтобы узнать мои возможности.')

bot.polling(non_stop = True)