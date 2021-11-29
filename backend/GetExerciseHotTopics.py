from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
import requests
from flask import request
import json
import numpy as np

app = Flask(__name__)



# Create Connection to the SQL Database
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

create_connection(db_name='group1',
                 db_user='admin_group1',
                 db_password="pXysH3Qdhz7ZLhkRgz89mTQCQG",
                 db_host='35.228.244.65',
                 db_port='5432')


engine = create_engine('postgresql://admin_group1:pXysH3Qdhz7ZLhkRgz89mTQCQG@35.228.244.65:5432/group1')


# Get ML assigned exercise
@app.route('/getexercisehot', methods=['GET', 'POST'])
def getexercisehot():

    # Post from frontend (STUDENT UI) - information about the student that opens the app
    hot_topics = json.loads(request.data)

    # First get the dataframe from the database.
    hot_topics_all = pd.read_sql('hot_topics_all', engine)
    tasks = pd.read_sql('tasks2', engine)

    # Merge the hot_topics_all and the tasks dataframe to receive the task for the given student and item_id
    hot_topics_all = pd.merge(hot_topics_all, tasks[["item_id", "block_name", "block_id", "task_id", "text"]],
                              how="left", on=["item_id"])

    # Select only the recommended student from the table.
    exercise_hot_topics = hot_topics_all[(hot_topics_all['name'] == hot_topics['name']) &
                                         (hot_topics_all['surname'] == hot_topics['surname'])]

    exercise_hot_topics = exercise_hot_topics.to_json()
    return exercise_hot_topics




"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Räto",'surname': "Kessler"}
response = requests.post('http://localhost:5000/getexercisehot', json=json_file)
print(response.text)
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

