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


# CREATE CONNECTION TO THE SQL
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




@app.route('/ml', methods=['GET', 'POST'])
def ml():
    # ML assign
    # Import required tables
    tasks = pd.read_sql('tasks2', engine)
    answers = pd.read_sql('answers2', engine)
    users = pd.read_sql('users2', engine)

    # load user name
    user_name = json.loads(request.data)

    # search user_id
    for row in range(len(users)):
        if users.loc[row, 'name'] == user_name['name'] and users.loc[row, 'surname'] == user_name['surname']:
            user_id_found = users.loc[row, 'user_id']

    # Create the merged ml table
    ml_df = pd.merge(tasks, answers, how="left", on=["task_id"])
    ml_df_user = ml_df[(ml_df['user_id'] == user_id_found)]

    # Extract the block id where the specific user has the most trouble
    ml_df_user.sort_values(by='duration', ascending = False)
    ml_block_id = ml_df_user['block_id'].iloc[0]

    # Assign exc with this specific block_id to the user
    ml_output = ml_df_user[(ml_df_user['block_id'] == ml_block_id)]

    # Return as json
    ml_output = ml_output.to_json()

    return ml_output


"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Räto",'surname': "Kessler"}
response = requests.post('http://localhost:5000/ml', json=json_file)
print(response.text)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)















