import datetime

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from loader import bot
from loguru import logger

from states.states_searching_for_hotel import SearchingForHotels

from functions.main_functions.find_cities import find_cities
from functions.main_functions.find_hotels import find_hotels
from functions.main_functions.find_photos import find_photos

from functions.additional_functions.total_search_result import total_search_result
from functions.additional_functions.currency_determination import currency_determination

from keyboards.inline.keyboard_cities import request_cities
from keyboards.inline.keyboard_currency import request_currency
from keyboards.inline.keyboard_language import request_language
from keyboards.inline.keyboard_find_photos import request_find_photos
from keyboards.reply.amount_hotels_photos import request_amount

from database.db import add_history

from datetime import date, timedelta
from classes.calendar_class import MyStyleCalendar


LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_searching_for_hotels(message: Message) -> None:
    """
    Функция "start_searching_for_hotels" обрабатывает команды "/lowprice" ("/highprice", "/bestdeal").
    Запрашивает у пользователя язык поиска.
    """

    bot.set_state(user_id=message.from_user.id, state=SearchingForHotels.language, chat_id=message.chat.id)
    send_mess = f'{message.from_user.first_name}, выберите язык поиска.'
    bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_language())
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data_info_search:
        if message.text == '/lowprice':
            data_info_search['command'] = 'lowprice'
        elif message.text == '/highprice':
            data_info_search['command'] = 'highprice'
        elif message.text == '/bestdeal':
            data_info_search['command'] = 'bestdeal'


@bot.callback_query_handler(func=lambda call: True, state=SearchingForHotels.language)
def language_get(call: CallbackQuery) -> None:
    """
    Функция "language_get" при получении информации от пользователя языка поиска,
    запрашивает название города для поиска наличия его в API Hotels.
    """

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    send_mess = f'{call.message.chat.first_name}, введите название города.'
    bot.send_message(chat_id=call.message.chat.id, text=send_mess, reply_markup=None)
    bot.set_state(user_id=call.message.chat.id, state=SearchingForHotels.find_city, chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id) as data_info_search:
        data_info_search['language'] = call.data


@bot.message_handler(content_types=['text'], state=SearchingForHotels.find_city)
def city_name_get(message: Message) -> None:
    """
    Функция "city_name_get" при получении названия города, в котором выполняется
    поиск отелей, проверяет наличие указанного населенного пункта в API Hotels.
    По результату поиска при нахождении нескольких населенных пунктов
    выполняет дополнительный запрос на уточнение населенного пункта.
    При возникновении ошибке или не был найден город выводит соответствующее сообщение, поиск прекращается.
    """

    bot.set_state(user_id=message.from_user.id, state=SearchingForHotels.find_city, chat_id=message.chat.id)
    send_mess = f'Выполняю поиск ...'
    bot.send_message(chat_id=message.chat.id, text=send_mess)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_info_search:
        found_cities = find_cities(city=message.text.title(), locale=data_info_search['language'])
    bot.delete_message(chat_id=message.chat.id, message_id=message.id + 1)
    if isinstance(found_cities, str) is True:
        bot.send_message(chat_id=message.chat.id, text=found_cities)
        bot.delete_state(message.from_user.id, message.chat.id)
    elif len(found_cities) == 0:
        send_mess = 'Ничего не было найдено, прошу уточнить название города.'
        bot.send_message(chat_id=message.chat.id, text=send_mess)
    else:
        send_mess = (f'В результате поиска были найдены следующие населенные пункты, '
                     f'прошу уточнить какой именно город мы рассматриваем:')
        bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_cities(found_cities))


@bot.callback_query_handler(func=lambda call: True, state=SearchingForHotels.find_city)
def cities_get(call: CallbackQuery) -> None:
    """
    Функция "cities_get" при получении уточняющей информации от пользователя о необходимом городе,
    запрашивает у пользователя валюту для определения цены проживания.
    """

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    send_mess = f'{call.message.chat.first_name}, в какой валюте вы хотели бы узнать цену проживания?'
    bot.send_message(chat_id=call.message.chat.id, text=send_mess, reply_markup=request_currency())
    bot.set_state(user_id=call.message.chat.id, state=SearchingForHotels.currency, chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id) as data_info_search:
        data_info_search['cityID'] = call.data


@bot.callback_query_handler(func=lambda call: True, state=SearchingForHotels.currency)
def currency_get(call: CallbackQuery) -> None:
    """
    Функция "currency_get" при получении информации от пользователя о необходимой валюте,
    запрашивает у пользователя дату заселения в отель.
    """

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')
    send_mess = f'{call.message.chat.first_name}, какого числа планируете заезд?'
    bot.send_message(chat_id=call.message.chat.id, text=send_mess)
    bot.set_state(user_id=call.message.chat.id, state=SearchingForHotels.checkin, chat_id=call.message.chat.id)
    with bot.retrieve_data(user_id=call.message.chat.id) as data_info_search:
        data_info_search['currency'] = call.data
    calendar, step = MyStyleCalendar(locale='ru', min_date=date.today()).build()
    bot.send_message(call.message.chat.id,
                     f"Выберите {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=MyStyleCalendar.func(), state=SearchingForHotels.checkin)
def calendar_checkin(call: CallbackQuery) -> None:
    """
    Функция "calendar_checkin" выполняет опрос по дате заезда, по окончанию опроса осуществляет
    запрос у пользователя даты выезда из отеля.
    """

    result, key, step = MyStyleCalendar(locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали дату заезда: {result.strftime('%d.%m.%Y')}",
                              call.message.chat.id,
                              call.message.message_id)
        bot.set_state(user_id=call.message.chat.id, state=SearchingForHotels.checkout, chat_id=call.message.chat.id)
        with bot.retrieve_data(user_id=call.message.chat.id) as data_info_search:
            data_info_search['checkin'] = result
            send_mess = f'{call.message.chat.first_name}, какого числа планируете выезд?'
            bot.send_message(chat_id=call.message.chat.id, text=send_mess)
            calendar, step = MyStyleCalendar(
                locale='ru',
                min_date=data_info_search['checkin'] + timedelta(days=1)
            ).build()
            bot.send_message(call.message.chat.id,
                             f"Выберите {LSTEP[step]}",
                             reply_markup=calendar)


@bot.callback_query_handler(func=MyStyleCalendar.func(), state=SearchingForHotels.checkout)
def calendar_checkout(call: CallbackQuery) -> None:
    """
    Функция "calendar_checkout" выполняет опрос по дате выезда.
    По окончанию опроса при выполнении команд "/lowprice" ("/highprice") выполняет
    запрос у пользователя количества выводимых отелей.
    При выполнении команды "/bestdeal" выполняет запрос у пользователя минимальной цены проживания в отеле.
    """

    with bot.retrieve_data(user_id=call.message.chat.id) as data_info_search:
        result, key, step = MyStyleCalendar(
            locale='ru',
            min_date=data_info_search['checkin'] + timedelta(days=1)
        ).process(call.data)
        if not result and key:
            bot.edit_message_text(f"Выберите {LSTEP[step]}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Вы выбрали дату выезда: {result.strftime('%d.%m.%Y')}",
                                  call.message.chat.id,
                                  call.message.message_id)
            data_info_search['checkout'] = result
            if data_info_search['command'] == 'lowprice' or data_info_search['command'] == 'highprice':
                bot.set_state(
                    user_id=call.message.chat.id,
                    state=SearchingForHotels.find_hotels,
                    chat_id=call.message.chat.id
                )
                send_mess = (f'Сколько отелей вам вывести?'
                             f'\nМаксимально выводимое число отелей 10 штук.')
                bot.send_message(chat_id=call.message.chat.id, text=send_mess, reply_markup=request_amount())
            elif data_info_search['command'] == 'bestdeal':
                bot.set_state(
                    user_id=call.message.chat.id,
                    state=SearchingForHotels.min_price,
                    chat_id=call.message.chat.id
                )
                currency = currency_determination(data=data_info_search['currency'])
                send_mess = f'Введите минимальную цену проживания за сутки в отеле в {currency}.'
                bot.send_message(chat_id=call.message.chat.id, text=send_mess)


@bot.message_handler(state=SearchingForHotels.min_price)
def min_price_get(message: Message) -> None:
    """
    Функций "min_price_get" проверяет информацию о минимальной цене, и при корректной информации запрашивает
    максимальную цену проживания за сутки.
    """

    send_mess = 'Введите, пожалуйста, целое число от 1'
    if message.text.isdigit() is False:
        bot.send_message(chat_id=message.chat.id, text=send_mess)
    elif int(message.text) < 1:
        bot.send_message(chat_id=message.chat.id, text=send_mess)
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_info_search:
            currency = currency_determination(data=data_info_search['currency'])
            send_mess = f'Введите максимальную цену проживания за сутки в отеле в {currency}.'
            bot.send_message(chat_id=message.chat.id, text=send_mess)
            bot.set_state(user_id=message.chat.id, state=SearchingForHotels.max_price, chat_id=message.chat.id)
            data_info_search['min_price'] = int(message.text)


@bot.message_handler(state=SearchingForHotels.max_price)
def max_price_get(message: Message) -> None:
    """
    Функций "max_price_get" проверяет информацию о максимальной цене, и при корректной информации запрашивает
    максимальную удаленность от центра выбранного населенного пункта.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_info_search:
        send_mess = f'Введите, пожалуйста, целое число больше {data_info_search["min_price"]}'
        if message.text.isdigit() is False:
            bot.send_message(chat_id=message.chat.id, text=send_mess)
        elif int(message.text) <= data_info_search["min_price"]:
            bot.send_message(chat_id=message.chat.id, text=send_mess)
        else:
            send_mess = (f'Введите максимальное расстояние от центра города. '
                         f'\nРасстояние укажите в километрах.')
            bot.send_message(chat_id=message.chat.id, text=send_mess)
            bot.set_state(user_id=message.chat.id, state=SearchingForHotels.distance, chat_id=message.chat.id)
            data_info_search['max_price'] = int(message.text)


@bot.message_handler(state=SearchingForHotels.distance)
def distance_get(message: Message) -> None:
    """
    Функций "distance_get" проверяет информацию о расстоянии до центра и при правильном указании
    выполняет запрос информации по отелям в городе в API Hotels.
    При отсутствии отелей в городе сообщает, что ничего не найдено.
    При нахождении отелей спрашивает у пользователя о необходимости вывода фотографий.
    """

    try:
        number = message.text.replace(',', '.')
        if float(number) > 0:
            send_mess = 'Выполняю поиск ...'
            bot.send_message(chat_id=message.chat.id, text=send_mess)
            try:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_info_search:
                    found_hotels = find_hotels(
                        command=data_info_search['command'],
                        city_id=data_info_search['cityID'],
                        checkin=data_info_search['checkin'],
                        checkout=data_info_search['checkout'],
                        locale=data_info_search['language'],
                        currency=data_info_search['currency'],
                        min_price=data_info_search['min_price'],
                        max_price=data_info_search['max_price'],
                        distance_to_center=(float(number))
                    )
                    bot.delete_message(chat_id=message.chat.id, message_id=message.id + 1)
                    if len(found_hotels) == 0:
                        send_mess = f'В выбранном вами городе (округе), отели не были найдены.'
                        bot.send_message(chat_id=message.chat.id, text=send_mess)
                        raise KeyError("Данные не найдены, поиск завершен")
                    elif isinstance(found_hotels, str) is True:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=found_hotels
                        )
                        raise KeyError("Данные не найдены, поиск завершен")
                    else:
                        bot.set_state(
                            user_id=message.from_user.id,
                            state=SearchingForHotels.find_photos,
                            chat_id=message.chat.id
                        )
                        send_mess = 'Вам необходимо вывести фотографии отеля?'
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=send_mess,
                            reply_markup=request_find_photos()
                        )
                        data_info_search['hotels'] = found_hotels
            except KeyError as exp:
                logger.exception(exp)
                bot.delete_state(message.from_user.id, message.chat.id)
        else:
            send_mess = f'Введите, пожалуйста, число больше 0.'
            bot.send_message(chat_id=message.chat.id, text=send_mess)
    except ValueError as exp:
        logger.exception(exp)
        send_mess = f'Введите, пожалуйста, число больше 0.'
        bot.send_message(chat_id=message.chat.id, text=send_mess)


@bot.message_handler(state=SearchingForHotels.find_hotels)
def amount_hotels_get(message: Message) -> None:
    """
    Функция "amount_hotels_get" проверяет введенное число и при правильном указании
    выполняет запрос информации по отелям в городе в API Hotels.
    При отсутствии отелей в городе сообщает, что ничего не найдено.
    При нахождении отелей спрашивает у пользователя о необходимости вывода фотографий.
    """

    send_mess = 'Введите, пожалуйста, целое число от 1 до 10'
    if message.text.isdigit() is False:
        bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_amount())
    elif int(message.text) < 1 or int(message.text) > 10:
        bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_amount())
    else:
        send_mess = 'Выполняю поиск ...'
        bot.send_message(chat_id=message.chat.id, text=send_mess)
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_info_search:
                found_hotels = find_hotels(
                    command=data_info_search['command'],
                    city_id=data_info_search['cityID'],
                    checkin=data_info_search['checkin'],
                    checkout=data_info_search['checkout'],
                    locale=data_info_search['language'],
                    currency=data_info_search['currency'],
                    amount=int(message.text),
                )
                bot.delete_message(chat_id=message.chat.id, message_id=message.id + 1)
                if len(found_hotels) == 0:
                    send_mess = f'В выбранном вами городе (округе), отели не были найдены.'
                    bot.send_message(chat_id=message.chat.id, text=send_mess)
                    raise KeyError("Данные не найдены, поиск завершен")
                elif isinstance(found_hotels, str) is True:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=found_hotels
                    )
                    raise KeyError("Данные не найдены, поиск завершен")
                else:
                    data_info_search['hotels'] = found_hotels
                    bot.set_state(
                        user_id=message.from_user.id,
                        state=SearchingForHotels.find_photos,
                        chat_id=message.chat.id
                    )
                    send_mess = 'Вам необходимо вывести фотографии отеля?'
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=send_mess,
                        reply_markup=request_find_photos()
                    )
        except KeyError as exp:
            logger.exception(exp)
            bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: True, state=SearchingForHotels.find_photos)
def answer_photos_get(call) -> None:
    """
    Функция "answer_photos_get" при положительном ответе задает вопрос пользователю
    о количестве выводимых фотографий, при отрицательном ответе выводит информацию
    по найденных отелям.
    """

    if call.data == 'yes':
        bot.set_state(
            user_id=call.message.chat.id,
            state=SearchingForHotels.amount_photos,
            chat_id=call.message.chat.id
        )
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        send_mess = (f'Сколько фотографий вам показать для каждого найденного отеля?'
                     f'\nМаксимально выводимое число фотографий 10 штук.')
        bot.send_message(chat_id=call.message.chat.id, text=send_mess, reply_markup=request_amount())
    else:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup='')
        with bot.retrieve_data(user_id=call.message.chat.id, chat_id=call.message.chat.id) as data_info_search:
            number_of_nights = (data_info_search["checkout"] - data_info_search["checkin"]).days
            hotels = ''
            for hotel in data_info_search['hotels']:
                if len(hotels) == 0:
                    hotels = hotel['name']
                else:
                    hotels = '; '.join([hotels, hotel['name']])
                send_mess = total_search_result(hotel, data_info_search, number_of_nights)
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text=send_mess,
                    disable_web_page_preview=True
                )
            history = (call.message.chat.id,
                       data_info_search["command"],
                       str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')),
                       hotels)
            add_history(history=history)
        bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)


@bot.message_handler(state=SearchingForHotels.amount_photos)
def amount_photos_get(message) -> None:
    """
    Функция "amount_photos_get" при корректном числе с указанием кол-ва фотографий,
    отправляет сообщение в чат с информацией о данных отелях и фотографии, для каждого отеля.
    """

    send_mess = 'Введите, пожалуйста, целое число от 1 до 10'
    if message.text.isdigit() is False:
        bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_amount())
    elif int(message.text) < 1 or int(message.text) > 10:
        bot.send_message(chat_id=message.chat.id, text=send_mess, reply_markup=request_amount())
    else:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data_info_search:
            number_of_nights = (data_info_search["checkout"] - data_info_search["checkin"]).days
            hotels = ''
            for hotel in data_info_search['hotels']:
                if len(hotels) == 0:
                    hotels = hotel['name']
                else:
                    hotels = '; '.join([hotels, hotel['name']])
                found_photos = find_photos(amount=int(message.text), hotel_id=hotel['hotel_id'])
                if isinstance(found_photos, str) is True:
                    bot.send_message(chat_id=message.chat.id, text=found_photos)
                    send_mess = total_search_result(hotel, data_info_search, number_of_nights)
                    bot.send_message(chat_id=message.chat.id, text=send_mess, disable_web_page_preview=True)
                else:
                    send_mess = total_search_result(hotel, data_info_search, number_of_nights)
                    media = list()
                    for photo in found_photos:
                        if len(media) == 0:
                            media.append(InputMediaPhoto(photo, caption=send_mess))
                        else:
                            media.append(InputMediaPhoto(photo))
                    bot.send_media_group(chat_id=message.chat.id, media=media)
            history = (message.from_user.id,
                       data_info_search["command"],
                       str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')),
                       hotels)
            add_history(history=history)
        bot.delete_state(message.from_user.id, message.chat.id)
