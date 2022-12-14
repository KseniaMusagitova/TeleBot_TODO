import random
import psycopg2

import telebot
from telebot import types

token = "5744384602:AAF0LAVfWPueld7p6jNthrpEc5fbJZO_i9E"

bot = telebot.TeleBot(token)

HELP = """
/help - display a list of available commands;
/add - add a task to the list (in the format: /add month/day task);
/show - print all added tasks;
/random - add a random task for Today."""

RANDOM_TASKS = ['первое', 'второе', 'третье']

tasks = {}

date = ""
task = ""



def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)


conn = psycopg2.connect('users.db')
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (1000,))

users = cursor.execute("SELECT * FROM 'users'")
print(users.fetchall())

conn.commit()

e




@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/help')
    itembtn2 = types.KeyboardButton('/add')
    itembtn3 = types.KeyboardButton('/show')
    markup.add(itembtn1, itembtn2, itembtn3)

    greetings = f'Hello, {message.from_user.first_name}! ' \
                f"\n" 'I am bot-todo! Here you can add a list of tasks for a particular day.'
    bot.send_message(message.chat.id, greetings, reply_markup=markup)



@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add"])
def add_date(message):
    bot.send_message(message.chat.id, "Enter the date in MM.DD format: ")
    bot.register_next_step_handler(message, add_task)


def add_task(message):
    global date
    date = message.text
    bot.send_message(message.chat.id, "Enter the task: ")
    bot.register_next_step_handler(message, received)


def received(message):
    global task
    task = message.text
    add_todo(date, task)
    bot.send_message(message.chat.id, f' Task {task}'
                                      f' has been added for the date {date}')
    print(tasks)


@bot.message_handler(commands=["random"])
def random_add(message):
    date = "Today"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = "Task -" + task + "- has been added for the date " + date
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["show", "print"])
def show_date(message):
    bot.send_message(message.chat.id, "Enter the date in MM.DD format: ")
    bot.register_next_step_handler(message, show_task)


def show_task(message):
    global task
    task = message.text
    global date
    date = message.text

    text = ""
    if date in tasks:
        text = date + "\n"
        for task in tasks[date]:
            text = text + "[] " + task + "\n"
    else:
        text = "No tasks"
    bot.send_message(message.chat.id, text)


# постоянно обращается к серверам телеграм
bot.polling(none_stop=True)