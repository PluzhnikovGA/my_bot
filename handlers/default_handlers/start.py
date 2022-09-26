from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'], state=None)
def start(message: Message) -> None:
    """
    Функция "start" обрабатывает команда "/start".
    Отправляет в чат сообщение, состоящее из следующей информации:
    - приветствие с пользователем;
    - представление названия бота;
    - представление информации для чего создан бот;
    - дана ссылка на команду /help, если человек не знает, что делать.
    """

    send_mess = (f'Добрый день, {message.from_user.first_name}!'
                 f'\nМое название "Choose a hotel for yourself"'
                 f'\nЯ бот для поиска отелей в интересующем вас городе.'
                 f'\nЕсли не знаете что делать, набери команду /help')
    bot.send_message(message.chat.id, send_mess)
