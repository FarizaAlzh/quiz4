import psycopg2

def insert_or_update_user(name, surname, phone):
    try:
        conn = psycopg2.connect(
            dbname="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("CALL insert_or_update_user(%s, %s, %s)", (name, surname, phone))
        conn.commit()
        print("Процедура успешно выполнена")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка:", error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    phone = input("Введите номер телефона: ")
    insert_or_update_user(name, surname, phone)
