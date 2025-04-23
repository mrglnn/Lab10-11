#2.1
import psycopg2
import csv

conn = psycopg2.connect(
    dbname="PhoneBook_DB",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


with open('/Users/margulanaman/Desktop/pp2_labs/File.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute(
            "INSERT INTO PhoneBook_DB (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
            (row['name'], row['phone'])
        )

conn.commit()
cursor.close()
conn.close()