from telegram_bot_calendar import DetailedTelegramCalendar


class MyStyleCalendar(DetailedTelegramCalendar):
    """
    Класс "MyStyleCalendar". Родительский класс "DetailedTelegramCalendar".
    Заменяет изображение клавиш "влево", "вправо".
    """

    prev_button = "⬅️"
    next_button = "➡️"
    empty_month_button = ""
    empty_year_button = ""
