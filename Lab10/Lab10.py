#2
import psycopg2


conn = psycopg2.connect(
    dbname="PhoneBook_DB",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()



name = input("Enter name: ")
phone = input("Enter phone: ")


cursor.execute("INSERT INTO PhoneBook_DB (name, phone) VALUES (%s, %s)", (name, phone))


conn.commit()
cursor.close()
conn.close()
