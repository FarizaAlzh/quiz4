import psycopg2

def get_contacts(search_term, limit, offset):
    try:
        conn = psycopg2.connect(
            dbname="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        if isinstance(search_term, str):
            query = "SELECT * FROM contacts WHERE first_name = %s LIMIT %s OFFSET %s"
            cur.execute(query, (search_term, limit, offset))
        elif isinstance(search_term, int):
            query = "SELECT * FROM contacts WHERE phone_number = %s LIMIT %s OFFSET %s"
            cur.execute(query, (str(search_term), limit, offset))
        else:
            raise ValueError("search_term must be a string (name) or an integer (phone number)")

        contacts = cur.fetchall()
        return contacts
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при получении контактов:", error)
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    search_term = input("Введите имя или номер телефона для поиска: ")
    limit = int(input("Введите лимит: "))
    offset = int(input("Введите смещение: "))

    # Вычисляем новое смещение для корректной пагинации
    new_offset = limit * (offset - 1)

    contacts = get_contacts(search_term, limit, new_offset)
    if contacts:
        print("Найденные контакты:")
        for contact in contacts:
            print(contact)
    else:
        print("Контакты не найдены.")


"""Лимит (Limit):
Лимит указывает, сколько записей должно быть возвращено результатом запроса.
Например, если вы установите лимит равным 10, запрос вернет только 10 записей из таблицы.
Лимит позволяет ограничить объем данных, возвращаемых из базы данных, что особенно полезно при работе с большими объемами данных.

Смещение (Offset):
Смещение определяет, с какой записи начать выборку данных.
Например, если у вас есть 100 записей в таблице, и вы устанавливаете смещение равным 10, запрос начнет выборку с 11-й записи и вернет следующие записи после нее.
Смещение позволяет пропустить определенное количество записей в начале результатов запроса и начать выборку с определенной позиции."""