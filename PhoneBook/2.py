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

# Запрос идентификатора контакта у пользователя
identifier = input("Введите имя или номер телефона контакта для обновления: ")

# Проверяем наличие контакта в таблице
cur.execute(
    "SELECT COUNT(*) FROM PhoneBook WHERE name = %s OR phone_number = %s",
    (identifier, identifier)
)
count = cur.fetchone()[0]
if count == 0:
    print("Контакт не найден.")
else:
    # Запрос новых данных у пользователя
    new_name = input("Введите новое имя (если не хотите менять, оставьте пустым): ")
    new_phone_number = input("Введите новый номер телефона (если не хотите менять, оставьте пустым): ")

    # Формируем запрос на обновление данных
    update_query = "UPDATE PhoneBook SET "
    update_values = []
    if new_name:
        update_query += "name = %s, "
        update_values.append(new_name)
    if new_phone_number:
        update_query += "phone_number = %s, "
        update_values.append(new_phone_number)
    # Убираем лишнюю запятую и пробел в конце запроса
    update_query = update_query.rstrip(", ")
    update_query += " WHERE name = %s OR phone_number = %s"
    update_values.extend([identifier, identifier])

    # Выполняем обновление данных
    cur.execute(update_query, update_values)
    print("Данные успешно обновлены.")

# Применяем изменения
conn.commit()

# Закрываем соединение
cur.close()
conn.close()
