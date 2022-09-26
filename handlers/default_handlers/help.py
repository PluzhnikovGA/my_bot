from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['help'], state=None)
def help_com(message: Message) -> None:
    """
    Функция "help_com" обрабатывает команда "/help".
    Отправляет в чат сообщение с командами, которые поддерживает бот.
    """

    send_mess = (f'Доступные команды:'
                 f'\n/lowprice - вывод самых дешёвых отелей в городе'
                 f'\n/highprice - вывод самых дорогих отелей в городе'
                 f'\n/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра'
                 f'\n/history - вывод истории поиска отелей')
    bot.send_message(message.chat.id, send_mess)
