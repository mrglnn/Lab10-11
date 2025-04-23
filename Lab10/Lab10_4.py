import psycopg2


conn = psycopg2.connect(
    dbname="PhoneBook_DB",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


name_to_delete = input("Enter name to delete: ")
phone_to_delete = input("Enter the phone number to delete: ")

cursor.execute("DELETE FROM PhoneBook_DB WHERE phone = %s", (phone_to_delete,))


cursor.execute("DELETE FROM PhoneBook_DB WHERE name = %s", (name_to_delete,))


conn.commit()
cursor.close()
conn.close()
