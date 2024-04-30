import csv
import psycopg2

def insert_from_csv(file_path):
    try:
        conn = psycopg2.connect(
            database="suppliers",  # Измените на имя вашей базы данных
            user="postgres",
            password="FALga814",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)  # Выводим содержимое каждой строки файла CSV
                name = row['name'].strip()
                phone = row['phone '].strip()  # Учитываем пробел после "phone"
                
                # Проверяем, существует ли уже запись с таким же именем и телефоном
                cur.execute("SELECT * FROM phonebooks WHERE Name = %s AND Phone = %s", (name, phone))
                if cur.fetchone():
                    print(f"Запись для {name} с телефоном {phone} уже существует. Пропускаем вставку.")
                    continue
                
                # Вставляем данные только если запись не найдена в базе данных
                cur.execute("INSERT INTO phonebooks (Name, Phone) VALUES (%s, %s)", (name, phone))

        conn.commit()
        print("Данные успешно добавлены в таблицу phonebooks из файла CSV.")
    except (Exception, psycopg2.Error) as e:
        print("Ошибка:", e)
    finally:
        cur.close()
        conn.close()

# Путь к вашему файлу CSV
file_path = 'data.csv'

# Вставка данных из файла CSV в таблицу PhoneBook
insert_from_csv(file_path)
