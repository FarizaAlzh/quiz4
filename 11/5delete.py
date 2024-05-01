import psycopg2

def delete_contact():
    try:
        conn = psycopg2.connect(
            dbname="suppliers",
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Запрашиваем метод удаления у пользователя
        deletion_method = input("Введите '1', чтобы удалить по имени пользователя, или '2', чтобы удалить по номеру телефона: ")

        if deletion_method == '1':
            username = input("Введите имя пользователя для удаления: ")
            query = "DELETE FROM contacts WHERE first_name = %s"
            cur.execute(query, (username,))
            print("Данные успешно удалены для контактов с именем пользователя:", username)
        elif deletion_method == '2':
            phone_number = input("Введите номер телефона для удаления: ")
            query = "DELETE FROM contacts WHERE phone_number = %s"
            cur.execute(query, (phone_number,))
            print("Данные успешно удалены для контактов с номером телефона:", phone_number)
        else:
            print("Неверный метод удаления. Пожалуйста, введите '1' или '2'.")

        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при удалении контактов:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    delete_contact()
