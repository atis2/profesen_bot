import telebot
from config import *
from logic import *

bot = telebot.TeleBot(Token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
        Привет! Я бот который будет тебе рекомендовать работу по твоими интересам по этой команде /work и просто присылать хорошо оплачиваемый работы /random!!!    \
""")

@bot.message_handler(commands=['random'])
def random(message): 
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = "пришли случайные профессию "
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)


@bot.message_handler(commands=['work'])
def random(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = message.text
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)

@bot.message_handler(commands=['pr'])
def random(message):
    name = message.from_user.username
    bot.send_chat_action(message.chat.id, 'typing')
    text = message.text[4:]
    add_info(name, text)
    bot.reply_to(message, "Готово!")




bot.infinity_polling()