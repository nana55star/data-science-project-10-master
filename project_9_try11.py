#table number 1 and 2 !!!!!!

import pandas as pd
import psycopg2
import datetime
connection = psycopg2.connect(user="postgres", password="barmej", host="127.0.0.1", port="5432", database="imdb_database")

cursor = connection.cursor()

cursor.execute("SELECT label_name, label_id FROM label_types")
result1 = cursor.fetchall()
labels = dict(result1)
labels

data = pd.read_csv('IMDB_Dataset.csv')
data.insert(0, 'id', range(1,1+len(data)))
data.insert(3, 'date', datetime.datetime.now().replace(microsecond=0))

data['sentiment']=[labels[x] for x in data['sentiment']]

for i,row in data.iterrows():
	row_ = tuple(row)
	sql1 = "INSERT INTO data_input4 (id, input_data, input_date) VALUES (%s,%s,%s)"
	cursor.execute(sql1, (row['id'],row['review'],datetime.datetime.now()))
	sql2 = "INSERT INTO data_labeling5 (id_label, Label_number,Label_date) VALUES (%s,%s,%s)"
	cursor.execute(sql2,(row['id'],row['sentiment'],datetime.datetime.now()))
	connection.commit()
