from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def request_language() -> InlineKeyboardMarkup:
    """
    Функция "request_language" создает клавиатуру для выбора языка поиска.

    :return: возвращает клавиатуру для выбора языка поиска.
    """

    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(
        text='Русский',
        callback_data='ru_RU'
    )
    button_2 = InlineKeyboardButton(
        text='Английский',
        callback_data='en_US'
    )
    keyboard.add(button_1, button_2)

    return keyboard
