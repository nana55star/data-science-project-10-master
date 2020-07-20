import psycopg2
import datetime
connection = psycopg2.connect(user="postgres", password="barmej", host="127.0.0.1", port="5432", database="imdb_database")

cursor = connection.cursor()
cursor.execute('SELECT * FROM data_input WHERE id <= 3')
try1=cursor.fetchall()
print(try1)
cursor.execute('SELECT id, input_date FROM data_input')
result = cursor.fetchall()
for id, input_date in result:
    cursor.execute('update data_input set input_date = %s where id = %s', (datetime.datetime.now(), id))
connection.commit()
cursor.execute('SELECT * FROM data_input WHERE id <= 3')
query1 = cursor.fetchall()
print(query1)

cursor.execute('SELECT * FROM data_input ORDER BY input_date ASC LIMIT 3')
query2 = cursor.fetchall()
print(query2)

cursor.execute('SELECT * FROM data_input ORDER BY input_date DESC LIMIT 3')
query3 = cursor.fetchall()
print(query3)

cursor.close()
connection.close()
