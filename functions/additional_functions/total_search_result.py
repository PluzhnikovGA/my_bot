from datetime import datetime


def total_search_result(hotel_info: dict, data_info_search: dict, number_of_nights: int) -> str:
    """
    Функция "total_search_result" обрабатывает собранные данные и подготавливает сообщение с информацией по отелю.

    :param hotel_info: информация по отелю;
    :param data_info_search: информация по запросу;
    :param number_of_nights: число ночей в отеле.

    :return: сообщение для отправки в чат телеграмм бота.
    """

    total_price = str(int(number_of_nights * round(hotel_info['exactCurrent'], 0)))
    if data_info_search['currency'] == 'RUB':
        total_price = ' '.join([total_price, 'RUB'])
    elif data_info_search['currency'] == 'USD':
        total_price = ''.join(['$', total_price])
    elif data_info_search['currency'] == 'EUR':
        total_price = ' '.join([total_price, '€'])
    send_mess = (f'Название отеля: {hotel_info["name"]}'
                 f'\nСайт отеля: http://www.hotels.com/ho{hotel_info["hotel_id"]}'
                 f'\nАдрес отеля: {hotel_info["address"]}'
                 f'\nРасстояние до центра выбранного города (округа): {hotel_info["distance to center"]}'
                 f'\nДата заезда: {datetime.strftime(data_info_search["checkin"], "%d.%m.%Y")}'
                 f'\nДата выезда: {datetime.strftime(data_info_search["checkout"], "%d.%m.%Y")}'
                 f'\nНочей в отеле: {number_of_nights}'
                 f'\nЦена номера за ночь: {hotel_info["price"]}'
                 f'\nОбщая цена за весь период проживания: {total_price}')
    return send_mess
