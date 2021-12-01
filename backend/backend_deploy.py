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




# Add new student
@app.route('/addstudent', methods=['GET', 'POST'])
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

# Assign hot topic exercise
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
    hot_topics_all.to_sql('hot_topics_all', engine, if_exists="replace", method='multi', index=False)

    return jsonify({'message': 'HotTopic assigned'})

# Delete a students
@app.route('/deletestudent', methods=['GET', 'POST'])
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

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    students = pd.read_sql('users2', engine)
    students = students.to_json()

    return students

# Get exercise hot topic
@app.route('/getexercisehot', methods=['GET', 'POST'])
def getexercisehot():

    # Post from frontend (STUDENT UI) - information about the student that opens the app
    hot_topics = json.loads(request.data)

    # First get the dataframe from the database.
    hot_topics_all = pd.read_sql('hot_topics_all', engine)
    hot_topics_all['item_id'] = hot_topics_all['item_id'].astype(float)
    tasks = pd.read_sql('tasks2', engine)

    # Merge the hot_topics_all and the tasks dataframe to receive the task for the given student and item_id
    hot_topics_all = pd.merge(hot_topics_all, tasks[["item_id", "block_name", "block", "task_id", "text"]],
                              how="left", on=["item_id"])

    # Select only the recommended student from the table.
    exercise_hot_topics = hot_topics_all[(hot_topics_all['name'] == hot_topics['name']) &
                                         (hot_topics_all['surname'] == hot_topics['surname'])]

    exercise_hot_topics = exercise_hot_topics.drop_duplicates(subset=['text'], keep='first')

    exercise_hot_topics = exercise_hot_topics.to_json()
    
    return exercise_hot_topics

# Get exercise machine learning
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
    ml_df_user.sort_values(by='duration', ascending=False, inplace=True)
    
    try:
        ml_block_name = ml_df_user['block_name'].iloc[0]

    # If no block id is found => new user, then assign block_id 1
    except:
        ml_block_name = 'Die Wanderung'


    # Assign exc with this specific block_id to the user
    ml_output = ml_df[(ml_df['block_name'] == ml_block_name)]
    ml_output.drop_duplicates(subset=['text'],inplace=True, keep='first')

    # Return as json
    ml_output = ml_output.to_json()


    return ml_output

# Get student progress
@app.route('/progress', methods=['GET', 'POST'])
def progress():
    propgress_items = pd.read_sql('progress_items2', engine)
    propgress_items = propgress_items.to_json()

    return propgress_items

# Return answer
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

# Upload word_info
@app.route('/uploadinfo', methods=['GET', 'POST'])
def uploadinfo():
    #new_word_info = json.loads(request.data)
    #new_word_info = pd.read_json(new_word_info)
    new_word_info = json.loads(request.data)
    new_word_info = pd.DataFrame.from_dict(new_word_info, orient='index')
    new_word_info = new_word_info.transpose()

    # Append the new rows to the word_info dataframe
    word_info = pd.read_sql('word_info2', engine)
    column_list = ['word_instance', "word_type", "basic_form", "level", "frequency"]
    new_word_info = new_word_info.set_axis(column_list, axis=1, inplace=False)
    word_info = word_info.append(new_word_info)

    # Create the instance_id's
    # Create column with numbering for the instance_id
    instance_id_list = ['instance_id_' + str(x) for x in range(len(word_info))]
    word_info["instance_id"] = instance_id_list

    # Reset the index to structure the index column
    word_info = pd.DataFrame(word_info.reset_index())
    word_info = word_info.drop(columns='index')

    # Write the updated word_info into the database
    word_info.to_sql('word_info2', engine, if_exists="replace", method='multi', index=False)

    # Update tasks since tasks is linked via instance_id
    tasks = pd.read_sql('tasks2', engine)
    tasks = tasks.drop(columns='instance_id')
    tasks = pd.merge(tasks, word_info[["word_instance", "word_type", "basic_form", "instance_id"]],
                     how="left", on=["word_instance", "word_type", "basic_form"])

    # Write the updated tasks into the database
    tasks.to_sql('tasks2', engine, if_exists="replace", method='multi', index=False)

    return jsonify({'message': 'word_info uploaded'})
# Upload exercise
@app.route('/uploadexc', methods=['GET','POST'])
def uploadexc():
    #new_word_info = json.loads(request.data)
    #new_word_info = pd.read_json(new_word_info)
    new_word_info = json.loads(request.data)
    new_word_info = pd.DataFrame.from_dict(new_word_info, orient='index')
    new_word_info = new_word_info.transpose()

    upload = new_word_info
    #####################################################
    ####### FIRST CONDITION IS FOR ######################
    ####### TASK META VERBS #############################
    #####################################################

    #####################################################
    ####### FIRST CONDITION IS FOR ######################
    ####### TASK META VERBS #############################
    #####################################################

    if upload.iloc[0]['word_type'] == 'verb':
        # --------------------------------------------------------#
        # --------- APPEND TO INSTRUCTION TABLE ------------------#
        # --------------------------------------------------------#

        new_TMverbs = upload

        # Add the new entries to the text column
        instructions = pd.read_sql('instructions2', engine)
        instructions = instructions.append(new_TMverbs[['text']])
        # After appending we want to assign the instruction_id's again.
        # Then the new entries also have an id.
        instruction_id_list = ["instruction_id_" + str(x) for x in range(len(instructions))]
        instructions["instruction_id"] = instruction_id_list
        # Reset the index to structure the index column
        instructions = pd.DataFrame(instructions.reset_index())
        instructions = instructions.drop(columns='index')
        # Write the updated tasks into the database

        instructions.to_sql('instructions2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO task_meta_verbs TABLE --------------#
        # --------------------------------------------------------#

        # Get task_meta_verbs from database
        task_meta_verbs = pd.read_sql("task_meta_verbs2", engine)

        # We need several columns
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id",
                       "block", "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                       "wordcloud", "instruction_id", "type", "modus", "tempus", "person"]  # "word_number",

        new_TMverbs = new_TMverbs[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id",
                                   "block", "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                   "wordcloud", "instruction_id", "type", "modus", "tempus",
                                   "person"]]  # "word_number",

        new_TMverbs = new_TMverbs.set_axis(column_list, axis=1, inplace=False)

        # Append new rows
        task_meta_verbs = task_meta_verbs.append(new_TMverbs)

        # Reset the index to structure the index column
        task_meta_verbs = pd.DataFrame(task_meta_verbs.reset_index())
        task_meta_verbs = task_meta_verbs.drop(columns='index')

        # Write the updated word_info into the database
        task_meta_verbs.to_sql('task_meta_verbs2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO tasks TABLE ------------------------#
        # --------------------------------------------------------#

        # Import all three tables apart from task_meta_verbs
        task_meta_verbs = pd.read_sql("task_meta_verbs2", engine)
        task_meta_prepositions = pd.read_sql("task_meta_prepositions2", engine)
        task_meta_other = pd.read_sql("task_meta_other2", engine)
        instructions = pd.read_sql("instructions2", engine)

        # We need several columns from several df's.
        tasks = task_meta_verbs[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                 "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]]

        tasks = tasks.append(task_meta_prepositions[
                                 ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                  "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                  "wordcloud"]],
                             ignore_index=True)

        tasks = tasks.append(
            task_meta_other[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                             "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]],
            ignore_index=True)

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # Change the column names referring to the illustration.
        # column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
        # "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        # tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        # tasks = pd.merge(tasks, instructions, how='left', on='text')
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



        # Generate task_id column as unique identifier
        task_id_list = ["task_id_" + str(x) for x in range(len(tasks))]
        tasks["task_id"] = task_id_list

        # Write tasks into database
        tasks.to_sql('tasks2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- LINK TM-TABLES TO TASKS WITH task_id ---------#
        # --------------------------------------------------------#

        # Link the meta-tables with tasks by task_id
        task_meta_verbs = pd.merge(task_meta_verbs, tasks[["basic_form", "task_id"]], how="left",
                                   on=["basic_form", "task_id"])
        task_meta_prepositions = pd.merge(task_meta_prepositions, tasks[["text", "task_id"]], how="left",
                                          on=["text", "task_id"])
        task_meta_other = pd.merge(task_meta_other, tasks[["text", "task_id"]], how="left", on=["text", "task_id"])

        # Write the meta-tables in the database
        task_meta_verbs.to_sql('task_meta_verbs2', engine, if_exists="replace", method='multi', index=False)
        task_meta_prepositions.to_sql('task_meta_prepositions2', engine, if_exists="replace", method='multi',
                                      index=False)
        task_meta_other.to_sql('task_meta_other2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------------------------------------------------------#
        # --------------------------------------------------------#

    #####################################################
    ####### SECOND CONDITION IS FOR #####################
    ####### TASK META PREPOSITION #######################
    #####################################################

    elif upload.iloc[0]['word_type'] == 'preposition':
        # if upload.iloc[0]['word_type'] == 'preposition':
        # --------------------------------------------------------#
        # --------- APPEND TO INSTRUCTION TABLE ------------------#
        # --------------------------------------------------------#

        new_TMprepositions = upload

        # Add the new entries to the text column
        instructions = pd.read_sql('instructions2', engine)
        instructions = instructions.append(new_TMprepositions[['text']])
        # After appending we want to assign the instruction_id's again.
        # Then the new entries also have an id.
        instruction_id_list = ["instruction_id_" + str(x) for x in range(len(instructions))]
        instructions["instruction_id"] = instruction_id_list
        # Reset the index to structure the index column
        instructions = pd.DataFrame(instructions.reset_index())
        instructions = instructions.drop(columns='index')

        # Write the updated tasks into the database
        instructions.to_sql('instructions2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO task_meta_prepositions TABLE -------#
        # --------------------------------------------------------#

        # Get task_meta_prepositions from database
        task_meta_prepositions = pd.read_sql("task_meta_prepositions2", engine)

        # We need several columns
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                       "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        new_TMprepositions = new_TMprepositions[
            ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
             "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]]

        new_TMprepositions = new_TMprepositions.set_axis(column_list, axis=1, inplace=False)

        # Append new rows
        task_meta_prepositions = task_meta_prepositions.append(new_TMprepositions)

        # Reset the index to structure the index column
        task_meta_prepositions = pd.DataFrame(task_meta_prepositions.reset_index())
        task_meta_prepositions = task_meta_prepositions.drop(columns='index')

        # Write the updated word_info into the database
        task_meta_prepositions.to_sql('task_meta_prepositions2', engine, if_exists="replace", method='multi',
                                      index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO tasks TABLE ------------------------#
        # --------------------------------------------------------#

        # Import all three tables apart from task_meta_verbs
        task_meta_verbs = pd.read_sql("task_meta_verbs2", engine)
        task_meta_prepositions = pd.read_sql("task_meta_prepositions2", engine)
        task_meta_other = pd.read_sql("task_meta_other2", engine)
        instructions = pd.read_sql("instructions2", engine)

        # We need several columns from several df's.
        tasks = task_meta_verbs[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                 "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]]

        tasks = tasks.append(task_meta_prepositions[
                                 ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                  "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                  "wordcloud"]],
                             ignore_index=True)

        tasks = tasks.append(
            task_meta_other[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                             "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]],
            ignore_index=True)

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # Change the column names referring to the illustration.
        # column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
        #              "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        # tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        # tasks = pd.merge(tasks, instructions, how='left', on='text')
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # Generate task_id column as unique identifier
        task_id_list = ["task_id_" + str(x) for x in range(len(tasks))]
        tasks["task_id"] = task_id_list

        # Write tasks into database
        tasks.to_sql('tasks2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- LINK TM-TABLES TO TASKS WITH task_id ---------#
        # --------------------------------------------------------#

        # Link the meta-tables with tasks by task_id
        task_meta_verbs = pd.merge(task_meta_verbs, tasks[["basic_form", "task_id"]], how="left",
                                   on=["basic_form", "task_id"])
        task_meta_prepositions = pd.merge(task_meta_prepositions, tasks[["text", "task_id"]], how="left",
                                          on=["text", "task_id"])
        task_meta_other = pd.merge(task_meta_other, tasks[["text", "task_id"]], how="left", on=["text", "task_id"])

        # Write the meta-tables in the database
        task_meta_verbs.to_sql('task_meta_verbs2', engine, if_exists="replace", method='multi', index=False)
        task_meta_prepositions.to_sql('task_meta_prepositions2', engine, if_exists="replace", method='multi',
                                      index=False)
        task_meta_other.to_sql('task_meta_other2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------------------------------------------------------#
        # --------------------------------------------------------#


    #####################################################
    ####### ELSE CONDITION IS FOR #######################
    ####### TASK META OTHER #############################
    #####################################################

    else:

        # --------------------------------------------------------#
        # --------- APPEND TO INSTRUCTION TABLE ------------------#
        # --------------------------------------------------------#

        new_TMother = upload

        # Add the new entries to the text column
        instructions = pd.read_sql('instructions2', engine)
        instructions = instructions.append(new_TMother[['text']])
        # After appending we want to assign the instruction_id's again.
        # Then the new entries also have an id.
        instruction_id_list = ["instruction_id_" + str(x) for x in range(len(instructions))]
        instructions["instruction_id"] = instruction_id_list
        # Reset the index to structure the index column
        instructions = pd.DataFrame(instructions.reset_index())
        instructions = instructions.drop(columns='index')

        # Write the updated tasks into the database
        instructions.to_sql('instructions2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO task_meta_other TABLE --------------#
        # --------------------------------------------------------#

        # Get task_meta_verbs from database
        task_meta_other = pd.read_sql("task_meta_other2", engine)

        # We need several columns
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                       "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        new_TMother = new_TMother[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                   "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                   "wordcloud"]]

        new_TMother = new_TMother.set_axis(column_list, axis=1, inplace=False)

        # Append new rows
        task_meta_other = task_meta_other.append(new_TMother)

        # Reset the index to structure the index column
        task_meta_other = pd.DataFrame(task_meta_other.reset_index())
        task_meta_other = task_meta_other.drop(columns='index')

        # Write the updated word_info into the database
        task_meta_other.to_sql('task_meta_other2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- APPEND TO tasks TABLE ------------------------#
        # --------------------------------------------------------#

        # Import all three tables apart from task_meta_verbs
        task_meta_verbs = pd.read_sql("task_meta_verbs2", engine)
        task_meta_prepositions = pd.read_sql("task_meta_prepositions2", engine)
        task_meta_other = pd.read_sql("task_meta_other2", engine)
        instructions = pd.read_sql("instructions2", engine)

        # We need several columns from several df's.
        tasks = task_meta_verbs[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                 "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]]

        tasks = tasks.append(task_meta_prepositions[
                                 ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                                  "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                  "wordcloud"]],
                             ignore_index=True)

        tasks = tasks.append(
            task_meta_other[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block",
                             "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]],
            ignore_index=True)

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # Change the column names referring to the illustration.
        # column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
        #              "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        # tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        # tasks = pd.merge(tasks, instructions, how='left', on='text')
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # Drop duplicates.
        tasks.drop_duplicates()

        # Generate task_id column as unique identifier
        task_id_list = ["task_id_" + str(x) for x in range(len(tasks))]
        tasks["task_id"] = task_id_list

        # Write tasks into database
        tasks.to_sql('tasks2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------- LINK TM-TABLES TO TASKS WITH task_id ---------#
        # --------------------------------------------------------#

        # Link the meta-tables with tasks by task_id
        task_meta_verbs = pd.merge(task_meta_verbs, tasks[["basic_form", "task_id"]], how="left",
                                   on=["basic_form", "task_id"])
        task_meta_prepositions = pd.merge(task_meta_prepositions, tasks[["text", "task_id"]], how="left",
                                          on=["text", "task_id"])
        task_meta_other = pd.merge(task_meta_other, tasks[["text", "task_id"]], how="left", on=["text", "task_id"])

        # Write the meta-tables in the database
        task_meta_verbs.to_sql('task_meta_verbs2', engine, if_exists="replace", method='multi', index=False)
        task_meta_prepositions.to_sql('task_meta_prepositions2', engine, if_exists="replace", method='multi',
                                      index=False)
        task_meta_other.to_sql('task_meta_other2', engine, if_exists="replace", method='multi', index=False)

        # --------------------------------------------------------#
        # --------------------------------------------------------#

    return jsonify({'message': 'exercises uploaded'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








