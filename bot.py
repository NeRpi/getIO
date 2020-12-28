import telebot
import robot

TOKEN = '1346716396:AAGuyz5kFdw62HlmuzeXP7vuAo34vbNkcbA'
bot = telebot.TeleBot(TOKEN)

# Цифровые выходы
keys = [telebot.types.InlineKeyboardButton('', callback_data='')]*16
# Выходы инструмента
buttons = [telebot.types.InlineKeyboardButton('', callback_data='')]*2
condition = robot.get_input()

# Функция генерирует клавиатуру, в зависимости от нужд:
def generateKeyboard(act, i = 0):
    newKeyboard = telebot.types.InlineKeyboardMarkup()
    # Clear - чистая клавитура
    if act == 'Clear':
        for i in range(16):
            keys[i] = telebot.types.InlineKeyboardButton(str(i)+')⚪', callback_data=str(i))
            condition[i] = False
    # On/Off - включение/выключение iй кнопки
    if act == 'On':
        keys[i] = telebot.types.InlineKeyboardButton(str(i)+')🔵', callback_data='-' + str(i))
        condition[i] = True
    if act == 'Off':
        keys[i] = telebot.types.InlineKeyboardButton(str(i)+')⚪', callback_data=str(i))
        condition[i] = False
    # Now - текущее состояние кнопок
    if act == 'Now':
        value = robot.get_input()
        for i in range(16):
            if not value[i]:
                keys[i] = telebot.types.InlineKeyboardButton(str(i) + ')⚪', callback_data=str(i))
            else:
                keys[i] = telebot.types.InlineKeyboardButton(str(i) + ')🔵', callback_data='-' + str(i))
    # Back - возвращение в меню
    if act == 'Back':
        newKeyboard.row(
            telebot.types.InlineKeyboardButton('Состояния', callback_data='get-input'),
            telebot.types.InlineKeyboardButton('Задать выходы', callback_data='set-output'),
        )
        return newKeyboard

    newKeyboard = telebot.types.InlineKeyboardMarkup()
    newKeyboard.row(
        keys[0], keys[1], keys[2], keys[3]
    )
    newKeyboard.row(
        keys[4], keys[5], keys[6], keys[7]
    )
    newKeyboard.row(
        keys[8], keys[9], keys[10], keys[11]
    )
    newKeyboard.row(
        keys[12], keys[13], keys[14], keys[15]
    )
    newKeyboard.row(
        telebot.types.InlineKeyboardButton('Очистить', callback_data='Clear'),
        telebot.types.InlineKeyboardButton('Обновить', callback_data='Update'),
        telebot.types.InlineKeyboardButton('Назад', callback_data='Back')
    )
    return newKeyboard


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Запустились', reply_markup=generateKeyboard('Back'))

@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    # Состояния входов
    if call.data == 'get-input':
        ansver = robot.get_input()
        for i in range(16):
            send = str(i) + ') '
            if ansver[i]:
                send += '🔵'
            else:
                send += '⚪'
            bot.send_message(call.message.chat.id, send)

    # Состояния выходов
    if call.data == 'set-output':
        bot.send_message(call.message.chat.id, 'Состояния: ', reply_markup=generateKeyboard('Now'))
    # Обработчик кнопки Назад
    if call.data == 'Back':
        bot.edit_message_text(text='Меню',chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=generateKeyboard('Back'))
    # Обновление клавиатуры
    if call.data == 'Update':
        try:
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                            reply_markup=generateKeyboard('Now'))
        except:
            bot.send_message(call.from_user.id, 'Состояния свежие')


    # Вся логика для кнопок цифровых выходов
    for i in range(16):
        if call.data == str(i):
            robot.set_output(i)
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('On', i))
        elif call.data == '-' + str(i):
            robot.set_output(i)
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('Off', i))
        else:
            pass
    # Обработчик конпки Очистить
    if call.data == 'Clear':
        try:
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=generateKeyboard('Clear'))
            robot.set_output(-1)
        except:
            bot.send_message(call.from_user.id, 'Ничего не горит')

@bot.message_handler(content_types=['text'])
def send(message):
    bot.send_message(message.chat.id, 'Включён')

bot.polling(none_stop=True)
