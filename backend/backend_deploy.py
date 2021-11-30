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


# Get ML assigned exercise
@app.route('/assignhot', methods=['GET', 'POST'])
def assignhot():


    # TEACHER ASSIGNS
    # First get the dataframe from the database.
    hot_topics_all = pd.read_sql('hot_topics_all', engine)
    #users = pd.read_sql('users2', engine)

    # Post from frontend (TEACHER UI) - information about hot topics as dictionary
    hot_topics = json.loads(request.data)

    # Search the student in hisot_topics_all. Loop through the rows, assign the item_id to the student.
    for row in range(len(hot_topics_all)):
        if hot_topics_all.loc[row, 'name'] == hot_topics['name'] and hot_topics_all.loc[row, 'surname'] == hot_topics['surname']:
            hot_topics_all.loc[row, 'item_id'] = hot_topics['item_id']

    # Load it back into the database.
    hot_topics_all.to_sql('hot_topics_all', engine, if_exists="append", method='multi', index=False)

    return jsonify({'message': 'HotTopic assigned'})


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


@app.route('/students', methods=['GET'])
def get_students():
    students = pd.read_sql('users2', engine)
    students = students.to_json()

    return students


@app.route('/getexercisehot', methods=['GET', 'POST'])
def getexercisehot():

    # Post from frontend (STUDENT UI) - information about the student that opens the app
    hot_topics = json.loads(request.data)

    # First get the dataframe from the database.
    hot_topics_all = pd.read_sql('hot_topics_all', engine)
    hot_topics_all['item_id'] = hot_topics_all['item_id'].astype(float)
    tasks = pd.read_sql('tasks2', engine)

    # Merge the hot_topics_all and the tasks dataframe to receive the task for the given student and item_id
    hot_topics_all = pd.merge(hot_topics_all, tasks[["item_id", "block_name", "block_id", "task_id", "text"]],
                              how="left", on=["item_id"])

    # Select only the recommended student from the table.
    exercise_hot_topics = hot_topics_all[(hot_topics_all['name'] == hot_topics['name']) &
                                         (hot_topics_all['surname'] == hot_topics['surname'])]

    exercise_hot_topics = exercise_hot_topics.to_json()
    return exercise_hot_topics


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
    ml_df = pd.merge(tasks, answers, how="left", on=["task_id", "text"])
    ml_df_user = ml_df[(ml_df['user_id'] == user_id_found)]

    # Extract the block id where the specific user has the most trouble
    ml_df_user.sort_values(by='duration', ascending=False)
    ml_block_name = ml_df_user['block_name'].iloc[0]

    # If no block id is found => new user, then assign block_id 1
    if not ml_block_name:
        ml_block_name = 'Die Wanderung'


    # Assign exc with this specific block_id to the user
    ml_output = ml_df[(ml_df['block_name'] == ml_block_name)]
    ml_output.drop_duplicates(subset=['text'],inplace=True, keep='first')

    # Return as json
    ml_output = ml_output.to_json()


    return ml_output


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    propgress_items = pd.read_sql('progress_items2', engine)
    propgress_items = propgress_items.to_json()

    return propgress_items


@app.route('/returnanswer', methods=['GET', 'POST'])
def returnanswer():
    # get dataframe from the database.
    users = pd.read_sql('users2', engine)

    answers_returned = json.loads(request.data)
    #answers_returned = {'name': "Räto", 'surname': "Kessler", 'task_id': 130, 'duration': 110}


    user_id = users[(users['name'] == answers_returned['name'][0]) & (users['surname'] == answers_returned['surname'][0])]['user_id']

    # transform into df
    answers_returned = pd.DataFrame.from_dict(answers_returned, orient='index')
    answers_returned['user_id'] = user_id
    answers_returned = answers_returned.transpose().dropna(subset=['name','surname'])

    # Load it back into the database.
    answers_returned.to_sql('answers2', engine, if_exists="append", method='multi', index=False)

    return jsonify({'message': 'answer returned'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








