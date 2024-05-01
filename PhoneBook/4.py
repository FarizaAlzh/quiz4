import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="suppliers",
    user="postgres",
    password="FALga814",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Запрос имени или номера телефона для удаления у пользователя
delete_option = input("Выберите опцию удаления (1 - по имени, 2 - по номеру телефона): ")

if delete_option == "1":
    name_to_delete = input("Введите имя для удаления: ")
    # Выполняем запрос на удаление данных по имени
    cur.execute(
        "DELETE FROM PhoneBook WHERE name = %s",
        (name_to_delete,)
    )
    print("Данные успешно удалены.")
elif delete_option == "2":
    phone_to_delete = input("Введите номер телефона для удаления: ")
    # Выполняем запрос на удаление данных по номеру телефона
    cur.execute(
        "DELETE FROM PhoneBook WHERE phone_number = %s",
        (phone_to_delete,)
    )
    print("Данные успешно удалены.")
else:
    print("Неправильная опция удаления.")

# Применяем изменения
conn.commit()

# Закрываем соединение
cur.close()
conn.close()
