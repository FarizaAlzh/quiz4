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

# Запрос имени и номера телефона у пользователя
name = input("Введите имя: ")
phone_number = input("Введите номер телефона: ")

# Проверка наличия данных в таблице
cur.execute(
    "SELECT COUNT(*) FROM PhoneBook WHERE name = %s AND phone_number = %s",
    (name, phone_number)
)
count = cur.fetchone()[0]
if count == 0:
    # Если данных нет, выполняем вставку
    cur.execute(
        "INSERT INTO PhoneBook (name, phone_number) VALUES (%s, %s)",
        (name, phone_number)
    )
    print("Контакт успешно добавлен.")
else:
    print("Контакт уже существует в базе данных.")

# Применяем изменения
conn.commit()

# Закрываем соединение
cur.close()
conn.close()
