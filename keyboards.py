from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from trello import TrelloManager


def get_boards_btn(trello_username):
    boards_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    boards = TrelloManager(trello_username).get_boards()
    for board in boards:
        boards_btn.add(KeyboardButton(board.get("name")))
    return boards_btn
