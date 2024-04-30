import csv
import psycopg2

def create_phonebook_table():
    """ Создание таблицы phonebooks, если она не существует """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phonebooks (
                ID SERIAL PRIMARY KEY,
                Name VARCHAR(100),
                Phone VARCHAR(20)
            )
        ''')
        conn.commit()
        print("Таблица phonebooks успешно создана.")
    except psycopg2.Error as e:
        print("Ошибка при создании таблицы phonebooks:", e)
    finally:
        cur.close()
        conn.close()

def insert_from_csv(file_path):
    """ Вставка данных из CSV файла в таблицу phonebooks """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name'].strip()
                phone = row['Phone'].strip()
                cur.execute("INSERT INTO phonebooks (Name, Phone) VALUES (%s, %s)", (name, phone))

        conn.commit()
        print("Данные успешно добавлены в таблицу phonebooks из файла CSV.")
    except (Exception, psycopg2.Error) as e:
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

def insert_from_console():
    """ Ввод данных пользователем из консоли """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        name = input("Введите имя пользователя: ")
        phone = input("Введите номер телефона: ")

        cur.execute("INSERT INTO phonebooks (Name, Phone) VALUES (%s, %s)", (name, phone))

        conn.commit()
        print("Данные успешно добавлены в таблицу phonebooks.")
    except (Exception, psycopg2.Error) as e:
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

def update_phonebook_entry(user_id):
    """ Обновление данных в таблице """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        new_name = input("Введите новое имя пользователя (оставьте пустым, если не хотите изменять): ")
        new_phone = input("Введите новый номер телефона (оставьте пустым, если не хотите изменять): ")

        if new_name.strip() or new_phone.strip():
            if new_name.strip() and new_phone.strip():
                cur.execute("UPDATE phonebooks SET Name = %s, Phone = %s WHERE ID = %s", (new_name.strip(), new_phone.strip(), user_id))
            elif new_name.strip():
                cur.execute("UPDATE phonebooks SET Name = %s WHERE ID = %s", (new_name.strip(), user_id))
            elif new_phone.strip():
                cur.execute("UPDATE phonebooks SET Phone = %s WHERE ID = %s", (new_phone.strip(), user_id))

            conn.commit()
            print("Данные успешно обновлены в таблице phonebooks.")
        else:
            print("Ничего не изменилось. Укажите новое имя или телефон.")
    except (Exception, psycopg2.Error) as e:
        print("Ошибка при обновлении данных в таблице phonebooks:", e)
    finally:
        cur.close()
        conn.close()

def query_phonebook(filter_name=None, filter_phone=None):
    """ Запрос данных из таблицы с фильтрами """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        query = "SELECT * FROM phonebooks"
        conditions = []
        params = []

        if filter_name:
            conditions.append("Name = %s")
            params.append(filter_name)
        if filter_phone:
            conditions.append("Phone = %s")
            params.append(filter_phone)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("Нет данных для заданных критериев.")

    except (Exception, psycopg2.Error) as e:
        print("Ошибка при запросе данных из таблицы phonebooks:", e)
    finally:
        cur.close()
        conn.close()

def delete_from_phonebook(filter_name=None, filter_phone=None):
    """ Удаление данных из таблицы """
    try:
        conn = psycopg2.connect(
            database="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        query = "DELETE FROM phonebooks"
        conditions = []
        params = []

        if filter_name:
            conditions.append("Name = %s")
            params.append(filter_name)
        if filter_phone:
            conditions.append("Phone = %s")
            params.append(filter_phone)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        conn.commit()
        print("Данные успешно удалены из таблицы phonebooks.")

    except (Exception, psycopg2.Error) as e:
        print("Ошибка при удалении данных из таблицы phonebooks:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Загрузить данные из CSV файла")
        print("2. Ввести имя пользователя и телефон с консоли")
        print("3. Обновить данные в таблице (изменить имя пользователя или телефон)")
        print("4. Запросить данные из таблицы (с различными фильтрами)")
        print("5. Удалить данные из таблицы по имени пользователя или номеру телефона")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            file_path = input("Введите путь к файлу CSV: ")
            insert_from_csv(file_path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            user_id = input("Введите ID пользователя для обновления: ")
            update_phonebook_entry(user_id)
        elif choice == "4":
            filter_name = input("Введите имя для фильтрации (оставьте пустым, если не нужно): ")
            filter_phone = input("Введите телефон для фильтрации (оставьте пустым, если не нужно): ")
            query_phonebook(filter_name, filter_phone)
        elif choice == "5":
            filter_name = input("Введите имя пользователя для удаления: ")
            filter_phone = input("Введите номер телефона для удаления: ")
            delete_from_phonebook(filter_name, filter_phone)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")
