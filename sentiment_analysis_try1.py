from flask import Flask, request
import requests
from flask import jsonify

# Initialize flask application
app=Flask(__name__)

payload = {'count':1000, 'sort_order': 'ascending' }
result= requests.get("http://127.0.0.1:3000/get_data", payload, headers={'Content-Type': 'application/json'})
result_q = result.json()
text=[]
labels=[]
for i in range(len(result_q)):
    text.append(result_q[i][0])
    labels.append(result_q[i][1])

print("first text with id=1: " + str(text[0]) )
print("first label of the first text: " + str(labels[0]) )

# vectorizer
import pickle
#  rb
with open('model.pickle', 'rb') as file:
    model = pickle.load(file)
#
with open('vectorizer.pickle', 'rb') as file:
    vectorizer = pickle.load(file)

import re
def clean_text(text):
    text = text.lower()
    text = re.sub("@[a-z0-9_]+", ' ', text)
    text = re.sub("[^ ]+\.[^ ]+", ' ', text)
    text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
    text = re.sub("[^a-z\' ]", ' ', text)
    text = re.sub(' +', ' ', text)
    return text

result_dict = {0: 'negative', 1: 'positive'}
def get_sentiment(text):
   try:
       text = clean_text(text)
       vector = vectorizer.transform([text])
       result = model.predict(vector)
       return result[0]
   except:
       return "ERROR"

texts2=[]
for i in range(len(result_q)):
    sentiment = get_sentiment(result_q[i][0])
    texts2.append(sentiment)
print("First text after being cleaned and transformed to numbers of labels with id=1: " + str(texts2[0]))

payload_1 = {'label_name':'positive', 'count': 1000 }
result_1= requests.get("http://127.0.0.1:3000/get_data_count", payload_1, headers={'Content-Type': 'application/json'})
payload_2 = {'label_name':'negative', 'count': 1000 }
result_2= requests.get("http://127.0.0.1:3000/get_data_count", payload_2, headers={'Content-Type': 'application/json'})

def accuracy(x_test,y_test):
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(x_test,y_test)
    return print("The accuracy is " + str(accuracy) )

accuracy(labels, texts2)
