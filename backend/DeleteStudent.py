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




# DELETE STUDENT QUERY
@app.route('/deletestudent', methods=['GET','POST'])
def deletestudent():

    delete_student = json.loads(request.data)

    # Get the users table from the database
    users = pd.read_sql('users2', engine)

    # Select a student to delete. Loop through the rows, search for same value and drop the row.
    for row in range(len(users)):
        if users.loc[row, 'name'] == delete_student['name'] and users.loc[row, 'surname'] == delete_student['surname']:
            users = users.drop(row)

    # Upload the (whole) updated users table to the database
    users.to_sql('users2', engine, if_exists="replace", method='multi', index=False)



    return jsonify({'message': 'student deleted'})



"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Timon",'surname': "Bodmer"}
response = requests.post('http://localhost:5000/deletestudent', json=json_file)
print(response.text)
"""


print('finished')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
