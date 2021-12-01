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


#############
# word_info #
#############
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
                       "wordcloud", "instruction_id", "type", "modus", "tempus",  "person"] # "word_number",

        new_TMverbs = new_TMverbs[["word_instance", "word_type", "basic_form", "text", "task_level", "item_id",
                                   "block", "block_name", "paragraph_id", "paragraph_order", "task_order", "display",
                                   "wordcloud", "instruction_id", "type", "modus", "tempus",  "person"]] # "word_number",

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

        # Change the column names referring to the illustration.
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
                       "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        tasks = pd.merge(tasks, instructions, how='left', on='text')

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

        # Change the column names referring to the illustration.
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
                       "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        tasks = pd.merge(tasks, instructions, how='left', on='text')

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

        # Change the column names referring to the illustration.
        column_list = ["word_instance", "word_type", "basic_form", "text", "task_level", "item_id", "block_id",
                       "block_name", "paragraph_id", "paragraph_order", "task_order", "display", "wordcloud"]

        tasks = tasks.set_axis(column_list, axis=1, inplace=False)
        tasks = pd.merge(tasks, instructions, how='left', on='text')

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

"""
#FRONTEND
import requests
import pandas as pd
#verbs:
json_file = {'word_instance': {0: 1, 1: 1},
 'word_type': {0: 'verb', 1: 'verb'},
 'basic_form': {0: 'warten', 1: 'haben'},
 'text': {0: 'Der Patient [wartet] heute eine Stunde.',
  1: 'Der Patient [hat] auch gestern eine Stunde [gewartet]. '},
 'task_level': {0: 'A2', 1: 'A2'},
 'item_id': {0: 123, 1: 130},
 'block': {0: 1, 1: 2},
 'block_name': {0: 'Im Krankenhaus', 1: 'Im Krankenhaus'},
 'paragraph_id': {0: 1, 1: 1},
 'paragraph_order': {0: 1, 1: 1},
 'task_order': {0: 1, 1: 1},
 'display': {0: 'line-simple', 1: 'line-simple'},
 'wordcloud': {0: 'yes', 1: 'yes'},
 'instruction_id': {0: 5, 1: 5},
 'type': {0: 'main', 1: 'auxiliary'},
 'modus': {0: 'indicative', 1: 'indicative'},
 'tempus': {0: 'present', 1: 'present'},
 'number': {0: 'singular', 1: 'singular'},
 'person': {0: 3, 1: 3}}
 
#prepositions:
json_file = {'word_instance': {0: 1, 1: 1},
 'word_type': {0: 'preposition', 1: 'preposition'},
 'basic_form': {0: 'ab', 1: 'ab'},
 'text': {0: 'Der Vertrag gilt [ab] 2021.',
  1: 'Ich bin [ab] März arbeitslos.'},
 'task_level': {0: 'A1', 1: 'A1'},
 'item_id': {0: 108, 1: 108},
 'block': {0: 1, 1: 2},
 'block_name': {0: 'Rund um die Zeit', 1: 'Rund um die Zeit'},
 'paragraph_id': {0: 1, 1: 1},
 'paragraph_order': {0: 1, 1: 1},
 'task_order': {0: 1, 1: 1},
 'display': {0: 'line-simple', 1: 'line-simple'},
 'wordcloud': {0: 'yes', 1: 'yes'},
 'instruction_id': {0: 25, 1: 25},
 'didactical_level': {0: 'A1', 1: 'A1'},
 'function': {0: 'time', 1: 'time'},
 'distinction': {0: '0', 1: '0'},
 'aspect_1': {0: 'start', 1: 'start'},
 'aspect_2': {0: '0', 1: '0'},
 'expressing': {0: 'year', 1: 'month'},
 'used_with': {0: '0', 1: '0'},
 'number': {0: '0', 1: '0'},
 'gender': {0: '0', 1: '0'},
 'case': {0: 'D', 1: 'D'},
 'case_visibility': {0: 'no', 1: 'no'},
 'contraction': {0: 'no', 1: 'no'},
 'position': {0: 'front', 1: 'front'}}
 
#other
json_file = {'word_instance': {0: 1, 1: 1},
 'word_type': {0: 'article', 1: 'article'},
 'basic_form': {0: 'der', 1: 'der'},
 'text': {0: 'Der Mann beschreibt [den] Wanderern den Weg.',
  1: '[Die] Wanderer danken dem Mann.'},
 'task_level': {0: 'A1', 1: 'A1'},
 'item_id': {0: 82, 1: 82},
 'block': {0: 1, 1: 1},
 'block_name': {0: 'Die Wanderung', 1: 'Die Wanderung'},
 'paragraph_id': {0: 1, 1: 1},
 'paragraph_order': {0: 1, 1: 1},
 'task_order': {0: 1, 1: 2},
 'display': {0: 'line-simple', 1: 'line-simple'},
 'wordcloud': {0: 'no', 1: 'no'},
 'instruction_id': {0: 15, 1: 15},
 'word_case': {0: 'accusative', 1: 'nominative'},
 'word_number': {0: 'plural', 1: 'plural'},
 'gender': {0: '0', 1: '0'},
 'paradigm': {0: 'definite', 1: 'definite'},
 'type': {0: '0', 1: '0'},
 'grade': {0: '0', 1: '0'}}
response = requests.post('http://localhost:5000/uploadexc', json=json_file)
print(response.text)
"""


print('finished')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
