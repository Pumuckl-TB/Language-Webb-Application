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
@app.route('/getexerciseml', methods=['GET', 'POST'])
def getexerciseml():

    # load user name
    user_name = json.loads(request.data)

    # Get the tables from the database
    users = pd.read_sql('users2', engine)
    ml = pd.read_sql('rec_task_ML', engine)


    # search user
    for row in range(len(users)):
        if users.loc[row, 'name'] == user_name['name'] and users.loc[row, 'surname'] == user_name['surname']:
            user_id_found = users.loc[row, 'user_id']

            # search ml database
            for row2 in range(len(ml)):
                exercise = ml[(ml['user_id'] == user_id_found)]

    exercise = exercise.to_json()
    return exercise


"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Räto",'surname': "Kessler"}
response = requests.post('http://localhost:5000/getexerciseml', json=json_file)
print(response.text)
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

