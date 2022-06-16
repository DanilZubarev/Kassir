import telebot
from telebot import types
import time
import telegram_send
from Chek_on_server import cash, non_cash, date
from Save_tabl import save_tabl, cheak_kass, incass, total_kass

# Входные параметры
token = '5395458744:AAEnB73kduH7K9nASWH246-cmXhS34sl8r8'
bot = telebot.TeleBot(token)
kassa = {'start': '', 'cash': cash, 'end': '', 'expen': '', 'non_cash': non_cash, 'err_cash_coment': '', 'kass_non_cash':'',
         'kass': '', 'coment': '', 'data': date, 'err_cash': '', 'err_non_cash': '', 'err_non_cash_coment':''}
kassa_expen = 0

# Значения Kassa_expen: 1 - Инкасация, 2 - Комент к err_cash, 3 - Комент к expen,
#                       4 - Комент к err_non_cash_coment

# Блок управления команды Старт
@bot.message_handler(commands=['start'])
def start (message):
    global kassa_expen
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Да, Я готов!', callback_data= 'Yes1'))
    user = message.from_user.first_name
    bot.send_message(message.chat.id,f'Привет {user}, приступим к сдаче смены!', reply_markup = markup)
    global kassa
    kassa = {'start': '', 'cash': cash, 'end': '', 'expen': '', 'non_cash': non_cash, 'err_cash_coment': '', 'kass_non_cash': '',
             'kass': '', 'coment': '', 'data': date, 'err_cash': '', 'err_non_cash': '', 'err_non_cash_coment': ''}
    kassa_expen = 0

# Инкасация наличных
@bot.message_handler(commands=['take'])
def take(message):
    bot.send_message(message.chat.id, f'В кассе {total_kass()} рублей, введи сумму сколько забираешь.')
    global kassa_expen
    kassa_expen = 1

# Блок ответов на нажатие кнопок в сообщениях
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global kassa_expen
    if call.data == 'Yes1':
        bot.send_message(call.message.chat.id, 'Отлично, введи сумму наличных на начало смены!')
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                              text= 'Да, Я готов!', reply_markup = None)
    elif call.data == 'Yes2':
        bot.send_message(call.message.chat.id, 'Введи сумму на которую пополнял.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Да, пополнял!😔', reply_markup=None)
    elif call.data == 'No2':
        bot.send_message(call.message.chat.id, 'Как хорошо когда в кассе все четко!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нет, я красавчик!', reply_markup=None)
        kassa['err_cash'] = 0
        bot.send_message(call.message.chat.id, 'Введи сумму которую оставляешь на следующую смену!')
    elif call.data == 'Yes3':
        bot.send_message(call.message.chat.id, 'Введи сумму расходов!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Да.', reply_markup=None)
    elif call.data == 'No3':
        bot.send_message(call.message.chat.id, 'Отлично, расходы это лишнее!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нет.', reply_markup=None)
        kassa['expen'] = 0
        bot.send_message(call.message.chat.id, 'Напиши сумму которую сдаешь.')

    elif call.data == 'Yes4':
        bot.send_message(call.message.chat.id, 'Напиши итоговую сумму, если в терминале меньше чем по программе то пишешь '
                                               'со знаком минус, если больше то со знаком плюс.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Да, были!😔', reply_markup=None)
    elif call.data == 'No4':
        bot.send_message(call.message.chat.id, 'Хммм, где-то у тебя ошибка!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нет, я же красавчик!', reply_markup=None)
        kassa['err_non_cash'] = 0
        if kassa['kass_non_cash'] > kassa['non_cash']:
            err = kassa['kass_non_cash'] - kassa['non_cash']
            bot.send_message(call.message.chat.id, f'Сумма в чеке на {err} рублей больше чем в программе!')
            Eror(call.message)
        else:
            err = kassa['non_cash'] - kassa['kass_non_cash']
            bot.send_message(call.message.chat.id, f'Сумма в чеке на {err} рублей меньше чем в программе!')
            Eror(call.message)

# Блок ответов на сообщения пользователя
@bot.message_handler(content_types=['text'])
def text (message):
    global kassa_expen, cash, non_cash
    if kassa_expen == 1:                              # Инкасция
        player = message.from_user.first_name
        bot.send_message(message.chat.id, f'В кассе осталось {incass(int(message.text))} рублей.')
        telegram_send.send(messages=[f'Было проведена инкасация {player}, изьято {message.text} рублей.'])
        kassa_expen = 0
    elif kassa ['start'] == '':
        kassa ['start'] = int(message.text)
        start = kassa['start']
        bot.send_message(message.chat.id,f'На начало смены было {start} рублей!')
        time.sleep(1)
        bot.send_message(message.chat.id, f'За смену пришло {cash} рублей наличными!')
        time.sleep(1)
        markup = types.InlineKeyboardMarkup()
        yes_2 = types.InlineKeyboardButton('Да, пополнял!😔', callback_data='Yes2')
        no_2 = types.InlineKeyboardButton('Нет, я красавчик!', callback_data= 'No2')
        markup.add(yes_2,no_2)
        bot.send_message(message.chat.id, 'Пополнял аккаунты наличными за счет клуба?', reply_markup=markup)
    elif kassa['err_cash'] == '':
        kassa['err_cash'] = int(message.text)
        err_cash = kassa['err_cash']
        bot.send_message(message.chat.id,f'Пополнений за счет клуба было на {err_cash} рублей!')
        time.sleep(1)
        bot.send_message(message.chat.id,f'Кратко опиши за что было пополнение.')
        kassa_expen = 2
    elif kassa_expen == 2:
        kassa['err_cash_coment'] = message.text
        time.sleep(1)
        bot.send_message(message.chat.id, 'Вроде понятно')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Введи сумму которую оставляешь на следующую смену!')
        kassa_expen = 0
    elif kassa['end'] == '':
        kassa['end'] = int(message.text)
        end = kassa['end']
        bot.send_message(message.chat.id, f'На следующую смену осталось {end} рублей!')
        time.sleep(1)
        markup = types.InlineKeyboardMarkup()
        yes_3 = types.InlineKeyboardButton('Да.', callback_data='Yes3')
        no_3 = types.InlineKeyboardButton('Нет.', callback_data= 'No3')
        markup.add(yes_3,no_3)
        bot.send_message(message.chat.id, 'Были ли расходы за твою смену?', reply_markup=markup)
    elif kassa['expen'] == '':
        kassa['expen'] = int(message.text)
        expen = kassa['expen']
        bot.send_message(message.chat.id, f'За смену было потраченно {expen} рублей!')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Напиши на что пошли расходы')
        kassa_expen = 3
    elif kassa_expen == 3:
        kassa ['coment'] = message.text
        bot.send_message(message.chat.id, 'Вроде понятно')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Напиши сумму которую сдаешь.')
        kassa_expen = 0
    elif kassa['kass'] == '':
        kassa['kass'] = int(message.text)
        total = kassa['start'] + kassa['cash'] - kassa['end'] - kassa['expen'] - kassa['err_cash']
        if kassa['kass'] == total:
            bot.send_message(message.chat.id, 'Поздравляю, касса по наличным сошлась!')
            kass = kassa['kass']
            bot.send_message(message.chat.id, f'Общая сумма наличных {cheak_kass(kass)} рублей.')
            time.sleep(1)
            bot.send_message(message.chat.id, 'Закрой смену в терминале и введи c чека сумму безналичных оплат.')
        elif kassa['kass'] > total:
            err = kassa['kass'] - total
            bot.send_message(message.chat.id, f'Ты сдаешь на {err} рублей больше чем должен.')
            Eror(message)
        else:
            err = total - kassa['kass']
            bot.send_message(message.chat.id, f'Ты сдаешь на {err} рублей меньше чем должен.')
            Eror(message)
    elif kassa['kass_non_cash'] == '':
        kassa['kass_non_cash'] = int(message.text)
        bot.send_message(message.chat.id, f'По программе за смену пришло {non_cash} рублей безналом!')
        if kassa['kass_non_cash'] != non_cash:
            markup = types.InlineKeyboardMarkup()
            yes_4 = types.InlineKeyboardButton('Да, были!😔', callback_data='Yes4')
            no_4 = types.InlineKeyboardButton('Нет, я же красавчик!', callback_data= 'No4')
            markup.add(yes_4,no_4)
            bot.send_message(message.chat.id, 'Были ошибки по безналичной кассе?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, '🤘Поздравляю смена сдана! Желаю хорошо отдохнуть!🤘')
            kassa['err_non_cash'] = 0
            save_tabl(kassa)
            total = kassa['non_cash'] + kassa['err_non_cash'] + kassa['cash'] + kassa['err_cash']
            user = message.from_user.first_name
            telegram_send.send( messages = [f'Касса сдана {user}, доход за смену {total} рублей, в кассе {total_kass()} рублей'])
    elif kassa['err_non_cash'] == '':
        kassa['err_non_cash'] = int(message.text)
        bot.send_message(message.chat.id, f'Кратко опиши их.')
        kassa_expen = 4
    elif kassa_expen == 4:
        kassa['err_non_cash_coment'] = message.text
        time.sleep(1)
        bot.send_message(message.chat.id, 'Вроде понятно')
        if kassa['kass_non_cash'] == non_cash + kassa['err_non_cash']:
            bot.send_message(message.chat.id, '🤘Поздравляю смена сдана! Желаю хорошо отдохнуть!🤘')
            save_tabl(kassa)
            total = kassa['non_cash'] + kassa['err_non_cash'] + kassa['cash'] + kassa['err_cash']
            user = message.from_user.first_name
            telegram_send.send( messages = [f'Касса сдана {user}, доход за смену {total} рублей, в кассе {total_kass()} рублей'])
        elif kassa['kass_non_cash'] >  non_cash + kassa['err_non_cash']:
            err = kassa['kass_non_cash'] -  non_cash + kassa['err_non_cash']
            bot.send_message(message.chat.id, f'Сумма в чеке на {err} рублей больше чем в программе!')
            Eror(message)
        else:
            err =  non_cash + kassa['err_non_cash'] - kassa['kass_non_cash']
            bot.send_message(message.chat.id, f'Сумма в чеке на {err} рублей меньше чем в программе!')
            Eror(message)

# Функция отправки сообщения об ошибки подсчетов кассы
def Eror(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))
    bot.send_message(message.chat.id, 'Проверь все и начни заново!', reply_markup=markup)

# Постоянная работа бота
def start():
    bot.polling(non_stop = True)
try:
    start()
except Exception as ex:
    telegram_send.send(messages=[ex])
    time.sleep(60)
    start()