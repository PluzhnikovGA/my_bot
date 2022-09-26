import sqlite3
import os


def create_history() -> None:
    """
    Функция "create_history" используется для создания файла баз данных.
    """
    conn = sqlite3.connect('history.db', check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY autoincrement,
        id_user INTEGER,
        command TEXT,
        date TEXT,
        hotels TEXT)
    """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS cities(
            id_city INTEGER PRIMARY KEY,
            lat REAL,
            lon REAL)
        """)
    conn.commit()


def add_history(history: tuple) -> None:
    """
    Функция "add_history" добавляет данные в таблицу "history".

    :param history: Кортеж с информацией для внесения в таблицу "history".
    """

    path = os.path.abspath(os.path.join('database', 'history.db'))
    with sqlite3.connect(path, check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO history(id_user, command, date, hotels)
            VALUES(?, ?, ?, ?);""", history)
        con.commit()


def get_history(id_user: int) -> list:
    """
    Функция "get_data" возвращает 5 последних записей пользователя из таблицы "history".

    :param id_user: ID пользователя, для которого выполняется поиск истории.

    :return: возвращает список с 5 последними успешными запросами.
    """

    path = os.path.abspath(os.path.join('database', 'history.db'))
    with sqlite3.connect(path, check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT command, date, hotels
                        FROM history
                        WHERE id_user = {id_user}
                        ORDER BY id DESC;""")
        results = cur.fetchmany(5)

        return results


def add_city(city: tuple) -> None:
    """
    Функция "add_city" добавляет (обновляет) данные в таблицу "cities".

    :param city: Кортеж с информацией о городе для внесения в таблицу "cities".
    """

    path = os.path.abspath(os.path.join('database', 'history.db'))
    with sqlite3.connect(path, check_same_thread=False) as con:
        cur = con.cursor()
        info = cur.execute(f"""SELECT * FROM cities WHERE id_city = {city[0]};""")
        if info.fetchone() is None:
            cur.execute("""INSERT INTO cities(id_city, lat, lon)
                            VALUES(?, ?, ?);""", city)
        else:
            cur.execute(f"""UPDATE cities
                            SET lat={city[1]},
                                lon={city[2]}
                            WHERE id_city={city[0]};""")
        con.commit()


def get_city(id_city: int) -> list:
    """
    Функция "get_city" возвращает координаты центра населенного пункта из таблицы "cities".

    :param id_city: ID населенного пункта, в котором выполняется поиск отелей.

    :return: возвращает координаты центра населенного пункта.
    """

    path = os.path.abspath(os.path.join('database', 'history.db'))
    with sqlite3.connect(path, check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT lat, lon
                        FROM cities
                        WHERE id_city = {id_city};""")
        result = cur.fetchone()

        return result
