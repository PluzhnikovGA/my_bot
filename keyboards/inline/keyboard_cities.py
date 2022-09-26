from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from database.db import add_city


def request_cities(found_cities: List) -> InlineKeyboardMarkup:
    """
    Функция "request_cities" создает клавиатуру для выбора города.

    :param found_cities: список найденных городов.

    :return: возвращает клавиатуру для выбора города.
    """

    keyboard = InlineKeyboardMarkup(row_width=1)
    for city in found_cities:
        city_info = (city['destinationId'], city["lav"], city["lon"])
        button = InlineKeyboardButton(
            text=city['name'],
            callback_data=city['destinationId']
        )
        keyboard.add(button)
        add_city(city=city_info)

    return keyboard
