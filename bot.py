import telebot
from environs import Env

from trello import TrelloManager
from utils import write_chat_to_csv, check_chat_id_from_csv, get_trello_username_by_chat_id
from keyboards import get_boards_btn

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")


# /start
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum, ro'yxatdan o'tish uchun /register:")


@bot.message_handler(commands=["register"])
def register_handler(message):
    bot.send_message(message.chat.id, "Trello username yuboring:")
    bot.register_next_step_handler(message, get_trello_username)


# Trello username
def get_trello_username(message):
    if not check_chat_id_from_csv("chats.csv", message.chat.id):
        write_chat_to_csv("chats.csv", message)
        bot.send_message(message.chat.id, "Muvaffaqqiyatli qo'shildi")
    else:
        bot.send_message(message.chat.id, "Siz avval ro'yxatdan o'tgansiz")


@bot.message_handler(commands=["boards"])
def get_boards(message):
    if not check_chat_id_from_csv("chats.csv", message.chat.id):
        bot.send_message(message.chat.id, "Trello username topilmadi.")
    else:
        trello_username = get_trello_username_by_chat_id("chats.csv", message.chat.id)
        if trello_username:
            bot.send_message(message.chat.id, "Boards", reply_markup=get_boards_btn(trello_username))
        else:
            bot.send_message(message.chat.id, "Trello username not found.")


my_commands = [
    telebot.types.BotCommand("/start", "Boshlash"),
    telebot.types.BotCommand("/register", "Ro'yxatdan o'tish"),
    telebot.types.BotCommand("/boards", "Doskalarni ko'rish"),
    telebot.types.BotCommand("/help", "Yordam")
]

if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(my_commands)
    bot.infinity_polling()
