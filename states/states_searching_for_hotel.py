from telebot.handler_backends import State, StatesGroup


class SearchingForHotels(StatesGroup):
    """
    Класс "SearchingForHotels". Родительский класс StatesGroup.
    Служит для последовательного сбора информации для команд "/lowprice", "/highprice", "/bestdeal".
    """

    language = State()
    find_city = State()
    currency = State()
    checkin = State()
    checkout = State()
    min_price = State()
    max_price = State()
    distance = State()
    find_hotels = State()
    find_photos = State()
    amount_photos = State()
