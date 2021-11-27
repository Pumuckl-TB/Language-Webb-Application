from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine

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




# call that gets all students and returns as json
# can be executed either via browser or with curl in the terminal
# curl -i http://localhost:5000/students
@app.route('/students', methods=['GET'])
def get_students():
    students = pd.read_sql('users2', engine)
    students = students.to_json()

    return students


"""
# Alternative. Exactly the same but the to_json fct is different.
@app.route('/students', methods=['GET'])
def get_students():
    students = pd.read_sql('users2', engine)

    return jsonify({'students': students})
"""






