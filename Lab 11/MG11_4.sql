CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(user_name TEXT, user_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM PhoneBook_DB
    WHERE name = user_name OR phone = user_phone;
END;
$$;
