import telebot
from telebot import types
import time
from Chek_on_server import cash, non_cash, date
from Save_tabl import save_tabl, save_kass, incass, total_kass

# Входные параметры
token = '5395458744:AAEnB73kduH7K9nASWH246-cmXhS34sl8r8'
bot = telebot.TeleBot(token)
kassa = {'start': '', 'cash': cash, 'end': '', 'expen': '',
         'non_cash': non_cash, 'kass': '', 'coment':'', 'data': date }
kassa_expen = 0
#save_tabl(kassa)

# Блок управления команды Старт
@bot.message_handler(commands=['start'])
def start (message):
    global kassa_expen
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Да, Я готов!', callback_data= 'Yes1'))
    bot.send_message(message.chat.id,'Привет, приступим к сдаче смены!', reply_markup = markup)
    global kassa
    kassa = {'start': '', 'cash': cash, 'end': '', 'expen': '', 'non_cash': non_cash, 'kass': '', 'coment': '', 'data': date}
    kassa_expen = 0

# Инкасация наличных
@bot.message_handler(commands=['take'])
def take(message):
    bot.send_message(message.chat.id, f'В кассе {total_kass()} рублей, введи сумму сколько забираешь.')
    global kassa_expen
    kassa_expen = 4

# Блок ответов на нажатие кнопок в сообщениях
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'Yes1':
        bot.send_message(call.message.chat.id, 'Отлично, введи сумму наличных на начало смены!')
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                              text= 'Да, Я готов!', reply_markup = None)
    elif call.data == 'Yes2':
        bot.send_message(call.message.chat.id, 'Введи сумму расходов!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Да.', reply_markup=None)
    elif call.data == 'No2':
        bot.send_message(call.message.chat.id, 'Отлично, расходы это лишнее!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нет.', reply_markup=None)
        kassa['expen'] = 0
        global kassa_expen
        kassa_expen = 1
        bot.send_message(call.message.chat.id, 'Напиши сумму которую сдаешь.')


# Блок ответов на сообщения пользователя
@bot.message_handler(content_types=['text'])
def text (message):
    global kassa_expen, cash, non_cash
    if kassa_expen == 4:                              # Инкасция
        bot.send_message(message.chat.id, f'В кассе осталось {incass(int(message.text))} рублей.')
        kassa_expen = 0
    elif kassa ['start'] == '':
        kassa ['start'] = int(message.text)
        start = kassa['start']
        bot.send_message(message.chat.id,f'На начало смены было {start} рублей!')
        time.sleep(1)
        bot.send_message(message.chat.id, f'За смену пришло {cash} рублей наличными!')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Введи сумму которую оставляешь на следующую смену!')
    elif kassa['end'] == '':
        kassa['end'] = int(message.text)
        end = kassa['end']
        bot.send_message(message.chat.id, f'На следующую смену осталось {end} рублей!')
        time.sleep(1)
        markup = types.InlineKeyboardMarkup()
        yes_2 = types.InlineKeyboardButton('Да.', callback_data='Yes2')
        no_2 = types.InlineKeyboardButton('Нет.', callback_data= 'No2')
        markup.add(yes_2,no_2)
        bot.send_message(message.chat.id, 'Были ли расходы за твою смену?', reply_markup=markup)
    elif kassa_expen == 0:
        kassa['expen'] = int(message.text)
        expen = kassa['expen']
        bot.send_message(message.chat.id, f'За смену было потраченно {expen} рублей!')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Напиши на что пошли расходы')
        kassa_expen = 2
    elif kassa_expen == 2:
        kassa ['coment'] = message.text
        bot.send_message(message.chat.id, 'Вроде понятно')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Напиши сумму которую сдаешь.')
        kassa_expen = 3
    elif kassa['kass'] == '':
        kassa['kass'] = int(message.text)
        if kassa['kass'] == kassa['start'] + kassa['cash'] - kassa['end'] - kassa['expen']:
            bot.send_message(message.chat.id, 'Поздравляю, касса по наличным сошлась!')
            kass = kassa['kass']
            bot.send_message(message.chat.id, f'Общая сумма наличных {save_kass(kass)} рублей.')
            time.sleep(1)
            bot.send_message(message.chat.id, 'Закрой сменну в терминале и введи c чека сумму безналичных оплат.')
        elif kassa['kass'] > kassa['start'] + kassa['cash'] - kassa['end'] - kassa['expen']:
            err = kassa['kass'] - (kassa['start'] + kassa['cash'] - kassa['end'] - kassa['expen'])
            bot.send_message(message.chat.id, f'Ты сдаешь на {err} рублей больше чем должен.')
            Eror(message)
        else:
            err = (kassa['start'] + kassa['cash'] - kassa['end'] - kassa['expen'] - kassa['kass'])
            bot.send_message(message.chat.id, f'Ты сдаешь на {err} рублей меньше чем должен.')
            Eror(message)
    else:
        non_cash1 = int(message.text)
        bot.send_message(message.chat.id, f'По программе за смену пришло {non_cash} рублей безналом!')
        if non_cash1 == kassa['non_cash']:
            bot.send_message(message.chat.id, 'Поздравляю смена сдана! Желаю хорошо отдохнуть!')
            save_tabl(kassa)
        elif non_cash1 > kassa['non_cash']:
            err = non_cash1 - kassa['non_cash']
            bot.send_message(message.chat.id, f'Сумма в чеке на {err} рублей больше чем в программе!')
            Eror(message)
        else:
            err = kassa['non_cash'] - non_cash1
            bot.send_message(message.chat.id, f'Сумма в чеке на {err} рублей меньше чем в программе!')
            Eror(message)

# Функция отправки сообщения об ошибки подсчетов кассы
def Eror(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))
    bot.send_message(message.chat.id, 'Проверь все и начни заново!', reply_markup=markup)

# Постоянная работа бота
bot.polling(non_stop = True)
