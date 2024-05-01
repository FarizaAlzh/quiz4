import psycopg2
import csv

def connect_to_database():
    return psycopg2.connect(
        dbname="suppliers",
        user="postgres",
        password="FALga814",
        host="localhost",
        port="5432"
    )

def insert_from_csv(conn):
    cur = conn.cursor()

    with open('PhoneBook/data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            name, phone_number = row
            cur.execute(
                "SELECT COUNT(*) FROM PhoneBook WHERE name = %s AND phone_number = %s",
                (name, phone_number)
            )
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute(
                    "INSERT INTO PhoneBook (name, phone_number) VALUES (%s, %s)",
                    (name, phone_number)
                )
                print(f"Добавлен новый контакт: {name}, {phone_number}")
            else:
                print(f"Контакт {name}, {phone_number} уже существует в базе данных.")

    conn.commit()
    cur.close()

def insert_from_console(conn):
    cur = conn.cursor()

    name = input("Введите имя: ")
    phone_number = input("Введите номер телефона: ")

    cur.execute(
        "SELECT COUNT(*) FROM PhoneBook WHERE name = %s AND phone_number = %s",
        (name, phone_number)
    )
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO PhoneBook (name, phone_number) VALUES (%s, %s)",
            (name, phone_number)
        )
        print("Контакт успешно добавлен.")
    else:
        print("Контакт уже существует в базе данных.")

    conn.commit()
    cur.close()

def update_data(conn):
    cur = conn.cursor()

    identifier = input("Введите имя или номер телефона контакта для обновления: ")

    cur.execute(
        "SELECT COUNT(*) FROM PhoneBook WHERE name = %s OR phone_number = %s",
        (identifier, identifier)
    )
    count = cur.fetchone()[0]
    if count == 0:
        print("Контакт не найден.")
    else:
        new_name = input("Введите новое имя (если не хотите менять, оставьте пустым): ")
        new_phone_number = input("Введите новый номер телефона (если не хотите менять, оставьте пустым): ")

        update_query = "UPDATE PhoneBook SET "
        update_values = []
        if new_name:
            update_query += "name = %s, "
            update_values.append(new_name)
        if new_phone_number:
            update_query += "phone_number = %s, "
            update_values.append(new_phone_number)
        update_query = update_query.rstrip(", ")
        update_query += " WHERE name = %s OR phone_number = %s"
        update_values.extend([identifier, identifier])

        cur.execute(update_query, update_values)
        print("Данные успешно обновлены.")

    conn.commit()
    cur.close()

def query_data(conn):
    cur = conn.cursor()

    filter_option = input("Выберите опцию фильтрации (1 - по имени, 2 - по номеру телефона): ")

    if filter_option == "1":
        name_filter = input("Введите имя для фильтрации: ")
        cur.execute(
            "SELECT * FROM PhoneBook WHERE name = %s",
            (name_filter,)
        )
    elif filter_option == "2":
        phone_filter = input("Введите номер телефона для фильтрации: ")
        cur.execute(
            "SELECT * FROM PhoneBook WHERE phone_number = %s",
            (phone_filter,)
        )
    else:
        print("Неправильная опция фильтрации.")

    rows = cur.fetchall()
    if rows:
        print("Результаты запроса:")
        for row in rows:
            print(row)
    else:
        print("Нет данных, удовлетворяющих условиям запроса.")

    cur.close()

def delete_data(conn):
    cur = conn.cursor()

    delete_option = input("Выберите опцию удаления (1 - по имени, 2 - по номеру телефона): ")

    if delete_option == "1":
        name_to_delete = input("Введите имя для удаления: ")
        cur.execute(
            "DELETE FROM PhoneBook WHERE name = %s",
            (name_to_delete,)
        )
        print("Данные успешно удалены.")
    elif delete_option == "2":
        phone_to_delete = input("Введите номер телефона для удаления: ")
        cur.execute(
            "DELETE FROM PhoneBook WHERE phone_number = %s",
            (phone_to_delete,)
        )
        print("Данные успешно удалены.")
    else:
        print("Неправильная опция удаления.")

    conn.commit()
    cur.close()

def main():
    conn = connect_to_database()

    while True:
        print("\nВыберите действие:")
        print("1. Вставить данные из файла CSV")
        print("2. Вставить данные через консольный ввод")
        print("3. Обновить данные")
        print("4. Запросить данные")
        print("5. Удалить данные")
        print("6. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            insert_from_csv(conn)
        elif choice == "2":
            insert_from_console(conn)
        elif choice == "3":
            update_data(conn)
        elif choice == "4":
            query_data(conn)
        elif choice == "5":
            delete_data(conn)
        elif choice == "6":
            break
        else:
            print("Неправильный ввод. Пожалуйста, выберите номер действия из списка.")

    conn.close()

if __name__ == "__main__":
    main()
