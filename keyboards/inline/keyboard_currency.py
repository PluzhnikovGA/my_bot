from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def request_currency() -> InlineKeyboardMarkup:
    """
    Функция "request_currency" создает клавиатуру для выбора валюты для оплаты отеля.

    :return: возвращает клавиатуру для выбора валюты для оплаты отеля.
    """

    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(
        text='Рубль',
        callback_data='RUB'
    )
    button_2 = InlineKeyboardButton(
        text='Доллар',
        callback_data='USD'
    )
    button_3 = InlineKeyboardButton(
        text='Евро',
        callback_data='EUR'
    )
    keyboard.add(button_1, button_2, button_3)

    return keyboard
