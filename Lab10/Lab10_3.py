import psycopg2


conn = psycopg2.connect(
    dbname="PhoneBook_DB",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


name_to_search = input("Enter name to search: ")


cursor.execute("SELECT * FROM PhoneBook_DB WHERE name = %s", (name_to_search,))


records = cursor.fetchall()
for record in records:
    print(record)

phone_to_search = input("Enter phone number to search: ")
cursor.execute("SELECT * FROM PhoneBook_DB WHERE phone = %s", (phone_to_search,))

recordss = cursor.fetchall()
for record in recordss:
    print(record)




cursor.close()
conn.close()
