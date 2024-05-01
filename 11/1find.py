import psycopg2

def search_records(pattern):
    """Поиск записей в телефонной книге по заданному шаблону"""
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        # Создание курсора
        cursor = conn.cursor()
        # Выполнение SQL-запроса для поиска записей
        cursor.execute("""
            SELECT first_name, last_name, phone_number
            FROM contacts 
            WHERE 
                first_name ILIKE %s OR
                last_name ILIKE %s OR
                phone_number ILIKE %s
        """, ('%' + pattern + '%', '%' + pattern + '%', '%' + pattern + '%'))
        # Получение результатов запроса
        records = cursor.fetchall()
        return records
    except (psycopg2.DatabaseError, Exception) as error:
        # Обработка ошибок
        print("Ошибка:", error)
    finally:
        # Закрытие соединения и курсора
        if conn is not None:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # Ввод шаблона поиска с клавиатуры
    pattern = input("Введите шаблон поиска: ")
    # Вызов функции поиска записей
    records = search_records(pattern)
    if records:
        # Вывод результатов поиска
        print("Результаты поиска:")
        for record in records:
            print(record)
    else:
        print("Записи не найдены.")
