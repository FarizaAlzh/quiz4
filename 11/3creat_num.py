import psycopg2

def insert_users():
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            dbname="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        # Создаем объект-курсор для выполнения SQL-запросов
        cur = conn.cursor()

        # Получаем от пользователя количество и имена для вставки
        num_users = int(input("Введите количество пользователей для вставки: "))
        for i in range(num_users):
            first_name = input(f"Введите имя пользователя {i+1}: ")
            last_name = input(f"Введите фамилию пользователя {i+1}: ")
            phone_number = input(f"Введите номер телефона пользователя {i+1}: ")

            # Вставляем данные пользователя в таблицу contacts
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
            """, (first_name, last_name, phone_number))

        print("Все пользователи успешно добавлены.")

        # Фиксируем изменения в базе данных
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        # В случае ошибки выводим сообщение об ошибке
        print("Ошибка при добавлении пользователей:", error)
        # Откатываем транзакцию в случае ошибки
        conn.rollback()
    finally:
        # Закрываем курсор и соединение с базой данных
        cur.close()
        conn.close()

if __name__ == '__main__':
    insert_users()

