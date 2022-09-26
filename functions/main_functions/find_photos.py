import json
import requests
from loguru import logger
from typing import Any
from config_data.config import RAPID_API_KEY, RAPID_API_HOST, URL_PHOTOS, MISTAKE


def find_photos(amount: int, hotel_id: int) -> Any:
    """
    Функция "find_photos" выполняет поиск фотографий в API Hotels для каждого найденного отеля.

    :param amount: максимальное кол-во выводимых фотографий (м.б. меньше на самом сайте);
    :param hotel_id: ID отеля найденный функцией 'find_hotels'.

    :return: Возвращает общий список найденных фотографий, собранная информация о фотографиях создается по шаблону.
             При возникновении проблем с сервером, возвращает сообщение с ошибкой.
    """

    photos = list()
    photo = {
        'type': 0,
        'suffix': ''
    }

    querystring = {"id": f"{hotel_id}"}
    try:
        response = requests.get(
            url=URL_PHOTOS,
            headers={"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST},
            params=querystring,
            timeout=40
        )
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, json.decoder.JSONDecodeError) as exp:
        logger.exception(exp)
        return MISTAKE

    if response.status_code >= 400:
        return MISTAKE

    data_photos = json.loads(response.text)

    for one_photo in data_photos['hotelImages']:
        for size in one_photo['sizes']:
            if size['type'] > photo['type']:
                photo['type'] = size['type']
                photo['suffix'] = size['suffix']
        photo = one_photo['baseUrl'].format(size=photo['suffix'])
        photos.append(photo)
        photo = {
            'type': 0,
            'suffix': ''
        }
        amount -= 1
        if amount == 0:
            break

    return photos
