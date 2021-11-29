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
@app.route('/assignhot', methods=['GET', 'POST'])
def assignhot():


    # TEACHER ASSIGNS
    # First get the dataframe from the database.
    hot_topics_all = pd.read_sql('hot_topics_all', engine)
    users = pd.read_sql('users2', engine)

    # Post from frontend (TEACHER UI) - information about hot topics as dictionary
    hot_topics = json.loads(request.data)

    # Search the student in hot_topics_all. Loop through the rows, assign the item_id to the student.
    for row in range(len(users)):
        if hot_topics_all.loc[row, 'name'] == hot_topics['name'] and hot_topics_all.loc[row, 'surname'] == hot_topics['surname']:
            hot_topics_all.loc[row, 'item_id'] = hot_topics['item_id']

    # Load it back into the database.
    hot_topics_all.to_sql('hot_topics_all', engine, if_exists="replace", method='multi', index=False)

    return jsonify({'message': 'HotTopic assigned'})


"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Räto", 'surname': "Kessler", 'item_id': 130}
response = requests.post('http://localhost:5000/assignhot', json=json_file)
print(response.text)
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

