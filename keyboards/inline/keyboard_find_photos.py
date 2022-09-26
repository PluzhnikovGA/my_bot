from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def request_find_photos() -> InlineKeyboardMarkup:
    """
    Функция "request_find_photos" создает клавиатуру для ответа о поиске фотографий.

    :return: возвращает клавиатуру для ответа о поиске фотографий.
    """

    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(
        text='Да',
        callback_data='yes'
    )
    button_2 = InlineKeyboardButton(
        text='Нет',
        callback_data='no'
    )
    keyboard.add(button_1, button_2)

    return keyboard
