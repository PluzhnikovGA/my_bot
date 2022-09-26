import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_HOST = "hotels4.p.rapidapi.com"
URL_CITY = "https://hotels4.p.rapidapi.com/locations/v2/search"
URL_HOTELS = "https://hotels4.p.rapidapi.com/properties/list"
URL_PHOTOS = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

MISTAKE = """Возникли проблемы с сервером.
Запрос информации в данный момент не возможен.
Просим прощения за доставленные неудобства.
Попробуйте повторить запрос позже."""

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку")
)
