from telebot.types import Message

from database.db import get_history
from loader import bot


@bot.message_handler(commands=['history'], state=None)
def get_hist(message: Message) -> None:
    """
    Функция "get_hist" обрабатывает команду "/history".
    Выводит в чат сообщения с последними 5 успешными запросами от пользователя.
    """

    history = get_history(id_user=message.from_user.id)
    if len(history) == 0:
        send_mess = 'История ваших сообщений пустая.'
        bot.send_message(chat_id=message.chat.id, text=send_mess)
    else:
        for one_history in history:
            send_mess = (f'Команда: {one_history[0]}'
                         f'\nДата запроса: {one_history[1]}'
                         f'\nСписок отелей: {one_history[2]}')
            bot.send_message(chat_id=message.chat.id, text=send_mess)
