import psycopg2
from config import load_config

def create_phonebook_table():
    """ Создание таблицы PhoneBook в базе данных PostgreSQL """
    command = """
        CREATE TABLE PhoneBook (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(100),
            Phone VARCHAR(20)
        )
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Выполнение запроса на создание таблицы PhoneBook
                cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_phonebook_table()
