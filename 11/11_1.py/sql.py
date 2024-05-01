"""CREATE OR REPLACE PROCEDURE insert_users(
    user_list JSON
)
LANGUAGE plpgsql
AS $$
DECLARE
    user_record JSON;
    user_name VARCHAR;
    user_surname VARCHAR;
    user_phone VARCHAR;
    incorrect_data JSON[];
BEGIN
    -- Инициализируем массив некорректных данных
    incorrect_data := '[]';

    -- Итерируемся по списку пользователей
    FOR user_record IN SELECT * FROM json_array_elements(user_list)
    LOOP
        -- Извлекаем имя, фамилию и номер телефона из записи
        user_name := user_record->>'name';
        user_surname := user_record->>'surname';
        user_phone := user_record->>'phone';

        -- Проверяем корректность номера телефона
        IF LENGTH(user_phone) <> 11 OR user_phone !~ '^\d+$' THEN
            -- Если номер телефона некорректный, добавляем запись в массив некорректных данных
            incorrect_data := incorrect_data || json_build_object('name', user_name, 'surname', user_surname, 'phone', user_phone);
        ELSE
            -- Если номер телефона корректный, вставляем запись в таблицу
            INSERT INTO contacts (first_name, last_name, phone_number) VALUES (user_name, user_surname, user_phone);
        END IF;
    END LOOP;

    -- Возвращаем все некорректные данные
    SELECT json_agg(data) INTO incorrect_data FROM (SELECT * FROM json_array_elements_text(incorrect_data) AS data) AS result;
    SELECT incorrect_data;
END;
$$;
"""

