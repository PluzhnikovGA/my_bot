import math

from database.db import get_city


def get_distance(id_city: int, lan_hotel: float, lon_hotel: float) -> float:
    """
    Функция "get_distance" выполняет расчет расстояния от отеля до центра населенного пункта,
    в котором выполняется поиск отеля.

    :param id_city: ID города, в котором выполняется поиск отелей;
    :param lan_hotel: географическая широта отеля;
    :param lon_hotel: географическая долгота отеля.

    :return: расстояние в километрах от отеля до центра населенного пункта, в котором выполняется поиск.
    """

    lav_lon_city = get_city(id_city=id_city)
    lan_city = math.radians(lav_lon_city[0])
    lon_city = math.radians(lav_lon_city[1])
    lan_hotel = math.radians(lan_hotel)
    lon_hotel = math.radians(lon_hotel)
    diff_lav = lan_city - lan_hotel
    diff_lon = lon_city - lon_hotel
    distance = round(2 * 6372.795 * math.asin(math.sqrt((math.sin(diff_lav / 2)) ** 2 + math.cos(lan_hotel) *
                                                        math.cos(lan_city) * (math.sin(diff_lon / 2)) ** 2)), 1)

    return distance
