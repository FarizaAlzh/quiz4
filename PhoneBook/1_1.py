import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="suppliers",
    user="postgres",
    password="FALga814",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Открываем файл CSV
with open('PhoneBook/data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропускаем заголовок
    for row in reader:
        name, phone_number = row
        # Проверяем наличие данных в таблице
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
            print(f"Добавлен новый контакт: {name}, {phone_number}")
        else:
            print(f"Контакт {name}, {phone_number} уже существует в базе данных.")

# Применяем изменения
conn.commit()

# Закрываем соединение
cur.close()
conn.close()
