CREATE OR REPLACE PROCEDURE insert_or_update_user(user_name TEXT, user_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PhoneBook_DB WHERE name = user_name) THEN
        UPDATE PhoneBook_DB SET phone = user_phone WHERE name = user_name;
    ELSE
        INSERT INTO PhoneBook_DB(name, phone) VALUES (user_name, user_phone);
    END IF;
END;
$$;
CALL insert_or_update_user('Aman Margulan', '87001234567');