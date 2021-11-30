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



# ADD STUDENT QUERY
@app.route('/addstudent', methods=['GET','POST'])
def addstudent():

    # Get new student data
    student = json.loads(request.data)
    student_df = pd.read_json(student)
    student_df['user_id'] = 'new'
    student_df.to_sql('users2', engine, if_exists='append', method='multi', index=False)
    users = pd.read_sql("users2", engine)

    # Create a student id for the new_student
    for row in range(len(users)):
        if users.loc[row, 'user_id'] == "new":
            users.loc[row, 'user_id'] = ["user_id_" + str(np.random.randint(1000000, 9000000))]

    users.to_sql('users2', engine, if_exists='replace', method='multi', index=False)

    # Since we have a new student, we also have to append them to the hot_topics table
    # get hot_topics_all df from the database
    hot_topics_all = pd.read_sql('hot_topics_all', engine)

    # Append newly added student to hot_topics_all data table
    users = pd.read_sql("users2", engine)
    hot_topics_all = hot_topics_all.append(users.iloc[-1])

    # return hot_topics_all df back to the database
    hot_topics_all.to_sql('hot_topics_all', engine, if_exists="replace", method='multi', index=False)



    return jsonify({'message': 'student added'})

"""
#FRONTEND
import requests
import pandas as pd

json_file = '{"name":{"0":"Lampe"},"surname":{"0":"Bodmer12"},"email":{"0":"timon.bodmer@uzh.ch"},"exercise_duration":{"0":60},"objective":{"0":"A2"},"user_id":{"0":"new"}}'
response = requests.post('http://localhost:5000/addstudent', json=json_file)
print(response.text)
"""

print('finished')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
