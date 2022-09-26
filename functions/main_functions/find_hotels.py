import json
import re
import requests
from loguru import logger
from typing import Any
from config_data.config import RAPID_API_KEY, RAPID_API_HOST, URL_HOTELS, MISTAKE
from functions.additional_functions.distance_calculation import get_distance


def find_hotels(
        command: str,
        city_id: int,
        checkin: Any,
        checkout: Any,
        locale: str,
        currency: str,
        amount: int = 25,
        min_price: int = None,
        max_price: int = None,
        distance_to_center: float = None
) -> Any:
    """
    Функция "find_hotels" выполняет поиск отелей в API Hotels в раннее указанном населенном пункте.

    :param command: команда на поиск отеля по критерию;
    :param city_id: ID города, полученный в результате выполнения функции "find_city_id";
    :param checkin: дата заезда в отель;
    :param checkout: дата выезд из отеля;
    :param locale: язык поиска;
    :param currency: валюта для оплаты услуг проживания;
    :param amount: кол-во отелей, которое необходимо вывести, больше 10 отелей выводится не будет;
    :param min_price: минимальная цена проживания в отеле;
    :param max_price: максимальная цена проживания в отеле;
    :param distance_to_center: расстояние до центра города (округа).

    :return: Возвращает общий список найденных отелей, собранная информация об отеле создается по шаблону.
             При возникновении проблем с сервером, возвращает сообщение с ошибкой.
    """

    sort_order = ''
    if command == 'lowprice':
        sort_order = 'PRICE'
    elif command == 'highprice':
        sort_order = 'PRICE_HIGHEST_FIRST'
    elif command == 'bestdeal':
        sort_order = 'DISTANCE_FROM_LANDMARK'

    querystring = {
        "destinationId": f"{city_id}", "pageNumber": "1", "pageSize": f"{amount}",
        "checkIn": f"{checkin}", "checkOut": f"{checkout}", "adults1": "1", "priceMin": f"{min_price}",
        "priceMax": f"{max_price}", "sortOrder": f"{sort_order}", "locale": f"{locale}", "currency": f"{currency}"
    }
    try:
        response = requests.get(
            url=URL_HOTELS,
            headers={"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST},
            params=querystring,
            timeout=40
        )
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as exp:
        logger.exception(exp)
        return MISTAKE

    if response.status_code >= 400:
        return MISTAKE

    data_hotels = json.loads(response.text)

    hotel_info = {
        'hotel_id': '',
        'name': '',
        'address': '',
        'distance to center': '',
        'price': '',
        'exactCurrent': ''
    }

    hotels_info = list()

    for hotel in data_hotels['data']['body']['searchResults']['results']:
        distance = ''
        for landmark in hotel["landmarks"]:
            if locale == 'ru_RU':
                if landmark['label'] == "Центр города":
                    distance = landmark["distance"].replace(',', '.')
                    distance = float(re.match(pattern=r'\d+\.*\d*', string=distance).group())
                    break
            elif locale == 'en_US':
                if landmark['label'] == "City center":
                    distance = landmark["distance"]
                    distance = round(float(re.match(pattern=r'\d+\.*\d*', string=distance).group()) * 1.609, 1)
                    break
        if isinstance(distance, str) is True:
            distance = get_distance(
                id_city=city_id,
                lan_hotel=hotel['coordinate']['lat'],
                lon_hotel=hotel['coordinate']['lon']
            )

        if ((command == 'bestdeal' and distance <= distance_to_center)
                or command == 'lowprice' or command == 'highprice'):
            distance = str(distance).replace('.', ',')
            distance = ' '.join([distance, 'км'])
            hotel_info['hotel_id'] = hotel['id']
            hotel_info['name'] = hotel['name']
            try:
                hotel_info['address'] = hotel['address']['streetAddress']
            except KeyError as exp:
                logger.exception(exp)
                hotel_info['address'] = 'Информация отсутствует на сервере.'
            hotel_info['distance to center'] = distance
            hotel_info['price'] = hotel['ratePlan']['price']['current']
            hotel_info['exactCurrent'] = hotel['ratePlan']['price']['exactCurrent']

            hotels_info.append(hotel_info.copy())

    return hotels_info
