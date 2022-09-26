from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_amount() -> ReplyKeyboardMarkup:
    """
    Функция "request_currency" создает клавиатуру для выбора кол-ва выводимых отелей (фотографий).

    :return: Клавиатуру для выбора кол-ва выводимых отелей (фотографий).
    """

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = KeyboardButton(text='2')
    button_2 = KeyboardButton(text='3')
    button_3 = KeyboardButton(text='5')
    button_4 = KeyboardButton(text='10')
    keyboard.add(button_1, button_2, button_3, button_4)

    return keyboard
