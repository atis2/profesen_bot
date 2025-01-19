import telebot
from config import *
from logic import *

bot = telebot.TeleBot(Token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
        Привет! Я бот который будет тебе рекомендовать работу по твоими интересам по команде /pr ты пишешь свои интересы и хобби, по этой команде буду рекомендовать /works и просто присылать хорошо оплачиваемый работы /random , и еще команда /home чтобы узнать профессии которые работуют с дома!!!    \
""")

@bot.message_handler(commands=['random'])
def random(message): 
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = "пришли хорошо оплачиваемый профессию "
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)


@bot.message_handler(commands=['works'])
def random(message):
    name = message.from_user.username
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = get_info(name)
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)

@bot.message_handler(commands=['pr'])
def random(message):
    name = message.from_user.username
    bot.send_chat_action(message.chat.id, 'typing')
    text = message.text[4:]
    add_info(name, text)
    bot.reply_to(message, "Готово!")

@bot.message_handler(commands=['home'])
def random(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = "пришли профессию которые работуют с дома"
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)

@bot.message_handler(commands=['foto'])
def echo_message(message):
    name = message.from_user.username
    user_id = message.chat.id
    prompt = "Это картинка для человека который ишет работу по зтим преподчениям" + get_info(name)
    bot.reply_to(message, "Генерирую картинку, подожди 3 минуты")
    bot.send_chat_action(message.chat.id, 'typing')
    img = show(prompt)
    with open(img, 'rb') as photo:
        
        bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")


@bot.message_handler(commands=['work'])
def random(message):
    name = message.from_user.username
    bot.send_chat_action(message.chat.id, 'typing')
    pro = Profeson()
    text = "прислать ТОЛЬКО ОДНУ профессию " + get_info(name)
    pros = pro.Ai_start(text)
    bot.reply_to(message, pros)
    name = message.from_user.username
    user_id = message.chat.id
    prompt = pros
    bot.reply_to(message, "Генерирую картинку, подожди 3 минуты")
    bot.send_chat_action(message.chat.id, 'typing')
    img = show(prompt)
    with open(img, 'rb') as photo:
        
        bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")

bot.infinity_polling()