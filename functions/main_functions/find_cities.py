import json
import requests
import re
from loguru import logger
from typing import Any
from config_data.config import RAPID_API_KEY, RAPID_API_HOST, URL_CITY, MISTAKE


def find_cities(city: str, locale: str) -> Any:
    """
    Функция "find_cities" выполняет поиск городов в API Hotels.

    :param city: название города, в котором осуществляется поиск отелей;
    :param locale: язык поиска.

    :return: ID и название найденных городов (округов) или пустой список, если ничего не было найдено.
             При возникновении проблем с сервером, возвращает сообщение с ошибкой.
    """

    found_cities = list()
    querystring = {"query": f"{city}", "locale": f"{locale}"}
    try:
        response = requests.get(
            url=URL_CITY,
            headers={"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST},
            params=querystring,
            timeout=40
        )
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as exp:
        logger.exception(exp)
        return MISTAKE

    if response.status_code != 200:
        return MISTAKE

    data = json.loads(response.text)

    for suggestion in data.get("suggestions"):
        if suggestion['group'] == 'CITY_GROUP':
            data = suggestion.get('entities')
            for one_of_the_cities in data:
                name = ''.join(re.split(r'<\S\w*\s*\w*=*\'*\w*\'*>', one_of_the_cities["caption"]))
                city_info = {
                    "destinationId": one_of_the_cities["destinationId"],
                    'name': name,
                    'lav': one_of_the_cities["latitude"],
                    'lon': one_of_the_cities["longitude"]
                }
                found_cities.append(city_info)

            return found_cities
