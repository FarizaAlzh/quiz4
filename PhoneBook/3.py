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

# Запрос фильтрации данных у пользователя
filter_option = input("Выберите опцию фильтрации (1 - по имени, 2 - по номеру телефона): ")

if filter_option == "1":
    name_filter = input("Введите имя для фильтрации: ")
    # Выполняем запрос данных с фильтром по имени
    cur.execute(
        "SELECT * FROM PhoneBook WHERE name = %s",
        (name_filter,)
    )
elif filter_option == "2":
    phone_filter = input("Введите номер телефона для фильтрации: ")
    # Выполняем запрос данных с фильтром по номеру телефона
    cur.execute(
        "SELECT * FROM PhoneBook WHERE phone_number = %s",
        (phone_filter,)
    )
else:
    print("Неправильная опция фильтрации.")

# Получаем результаты запроса и выводим их
rows = cur.fetchall()
if rows:
    print("Результаты запроса:")
    for row in rows:
        print(row)
else:
    print("Нет данных, удовлетворяющих условиям запроса.")

# Закрываем соединение
cur.close()
conn.close()
