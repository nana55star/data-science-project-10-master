import sys
import psycopg2
from flask import Flask, jsonify
from flask import request

# Initialize flask application
app = Flask(__name__)


# Default route to 127.0.0.1:3000
@app.route('/')
def home():
    return "<h1> Hello Data Science Course! </h1>"


@app.route('/get_data_count', methods=['GET'])

def get_data_count():
    try:
        connection = psycopg2.connect(user="postgres", password="barmej", host="127.0.0.1", port="5432", database="imdb_database")
        cursor = connection.cursor()
        label_name = str(request.args.get('label_name'))
        count = int(request.args.get('count', default=50000))
        if label_name == 'positive':
            cursor.execute("SELECT id_label,label_number FROM data_labeling5 WHERE label_number = 1 AND id_label <= %s",[count])
            result2 = cursor.rowcount
        elif label_name == 'negative':
            cursor.execute("SELECT id_label,label_number FROM data_labeling5 WHERE label_number = 0 AND id_label <= %s",[count])
            result2 = cursor.rowcount
        return jsonify(result2)
    except:
        return "Sorry, there is an error in your input!"

@app.route('/get_data', methods=['GET'])

def get_data():
    try:
        connection = psycopg2.connect(user="postgres", password="barmej", host="127.0.0.1", port="5432", database="imdb_database")
        cursor = connection.cursor()
        count = int(request.args.get('count'))
        sort_order = str(request.args.get('sort_order'))
        if sort_order == 'ascending':
            cursor.execute("SELECT input_data,Label_number FROM data_input4 INNER JOIN data_labeling5 ON id = id_label ORDER BY input_date ASC LIMIT %s",[count])
            result = cursor.fetchall()
        elif sort_order == 'descending':
            cursor.execute("SELECT input_data,Label_number FROM data_input4 INNER JOIN data_labeling5 ON id = id_label ORDER BY input_date DESC LIMIT %s",[count])
            result = cursor.fetchall()
        return jsonify(result)
    except:
        return "Sorry, there is an error in your input!"

# Start REST.py on port 3000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)




