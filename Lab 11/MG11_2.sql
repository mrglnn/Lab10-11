CREATE OR REPLACE PROCEDURE insert_many_users(
    IN names TEXT[],
    IN phones TEXT[],
    OUT incorrect_data TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
BEGIN
    incorrect_data := ARRAY[]::TEXT[];

    WHILE i <= array_length(names, 1) LOOP
        IF phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            BEGIN
                INSERT INTO PhoneBook_DB(name, phone)
                VALUES (names[i], phones[i])
                ON CONFLICT (phone) DO NOTHING;
            EXCEPTION
                WHEN OTHERS THEN
                    incorrect_data := array_append(incorrect_data, names[i] || ':' || phones[i]);
            END;
        ELSE
            incorrect_data := array_append(incorrect_data, names[i] || ':' || phones[i]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;
