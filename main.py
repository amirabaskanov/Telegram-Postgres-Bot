import telebot
from telebot import types
import psycopg2
bot = telebot.TeleBot('980141424:AAE2ZoI0nJcrVfZSmzD0Li9wstxxvS2Goc0')

first_name = ''
last_name = ''
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/hi' or message.text == '/start':
        #postgres_create_query = 'CREATE TABLE IF NOT EXISTS cv (user_id INTEGER PRIMARY KEY , first_name VARCHAR(40), last_name VARCHAR(40));'

        a = str(message.from_user)
        bot.send_message(message.from_user.id, "What's Your name?")
        bot.register_next_step_handler(message, get_first_name)
        with open('cv.doc', 'a') as f:
            f.write(a + '\n')
    else:
        bot.send_message(message.from_user.id, 'Write /hi')


def get_first_name(message):
    global first_name
    a = first_name = message.text
    bot.send_message(message.from_user.id, "What's Your surname?")
    bot.register_next_step_handler(message, get_last_name)
    with open('cv.doc', 'a') as f:
        f.write(a + '\n')


def get_last_name(message):
    global last_name
    a = last_name = message.text
    bot.send_message(message.from_user.id, "How old are you?")
    bot.register_next_step_handler(message, get_age)
    with open('cv.doc', 'a') as f:
        f.write(a + '\n')


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)

        except Exception:
            bot.send_message(message.from_user.id, 'use numbers, please)');
        keyboard = types.InlineKeyboardMarkup();
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes');
        keyboard.add(key_yes);
        key_no = types.InlineKeyboardButton(text='No', callback_data='no');
        keyboard.add(key_no);
        question = 'You are ' + str(age) + ' years old, Your name is ' + first_name +\
                   ' ' + last_name + '.' + ' Want to save it?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        with open('cv.doc', 'a') as f:
            f.write(str(age) + '\n')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        try:
            connection = psycopg2.connect(user="amir",
                                          password="password1",
                                          host="localhost",
                                          port="5432",
                                          database="cv")
            cursor = connection.cursor()
            postgres_insert_query = "INSERT INTO cv (first_name,last_name,age) VALUES (%s,%s,%s)"
            record_to_insert = (first_name, last_name, age)
            cursor.execute(postgres_insert_query, record_to_insert, )
            connection.commit()
            bot.send_message(call.message.chat.id, 'Remember it: )')

        except (Exception, psycopg2.Error) as error:
            if (connection):
                print("Failed to insert record into mobile table", error)


    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Delete it: )')


bot.polling(none_stop=True, interval=0)