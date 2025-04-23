import psycopg2

conn = psycopg2.connect(
    dbname="PhoneBook_DB",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


name_to_update = input("Enter the name to update: ")
new_phone = input("Enter the new phone: ")


cursor.execute("UPDATE PhoneBook_DB SET phone = %s WHERE name = %s", (new_phone, name_to_update))


conn.commit()
cursor.close()
conn.close()
