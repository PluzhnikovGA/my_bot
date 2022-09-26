def currency_determination(data: str) -> str:
    """
    Функция "currency_determination" выполняет выбор названия валюты.

    :param data: сокращенное название валюты.

    :return: Название валюты, для возможности правильного указания ее в сообщении.
    """

    currency = ''
    if data == 'RUB':
        currency = 'рублях'
    elif data == 'USD':
        currency = 'долларах'
    elif data == 'EUR':
        currency = 'евро'

    return currency
