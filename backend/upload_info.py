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
@app.route('/uploadinfo', methods=['GET','POST'])
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

"""
#FRONTEND
import requests
import pandas as pd
json_file = {"instance":{"0":1,"1":1,"2":1,"3":1,"4":1,"5":2,"6":1,"7":1,"8":1,"9":1,"10":1,"11":1,"12":1,"13":1,"14":1,"15":1,"16":1,"17":1,"18":1,"19":1,"20":1,"21":1,"22":1,"23":1,"24":1,"25":1,"26":1,"27":1,"28":1,"29":2,"30":1,"31":1,"32":1,"33":1,"34":1,"35":1,"36":1,"37":1,"38":1},"type":{"0":"noun","1":"adjective","2":"adverb","3":"verb","4":"noun","5":"noun","6":"noun","7":"noun","8":"noun","9":"noun","10":"noun","11":"noun","12":"article","13":"article","14":"pronoun","15":"pronoun","16":"pronoun","17":"verb","18":"verb","19":"verb","20":"verb","21":"verb","22":"verb","23":"verb","24":"verb","25":"adjective","26":"adjective","27":"adjective","28":"adjective","29":"adverb","30":"adverb","31":"adverb","32":"numeral","33":"numeral","34":"connector","35":"connector","36":"connector","37":"preposition","38":"preposition"},"basic_form":{"0":"Mann","1":"schnell","2":"schnell","3":"waschen","4":"Teil","5":"Teil","6":"Portugiese","7":"Grieche","8":"Chinese","9":"Bulgare","10":"Franzose","11":"Finne","12":"der","13":"ein","14":"er","15":"sie","16":"es","17":"warten","18":"haben","19":"wollen","20":"essen","21":"d\u009frfen","22":"geben","23":"aufstehen","24":"k\u009annen","25":"nett","26":"jung","27":"klein","28":"schnell","29":"schnell","30":"heute","31":"hier","32":"drei","33":"dritt","34":"weil","35":"wenn","36":"und","37":"ab","38":"an"},"level":{"0":"A1","1":"A1","2":"A2","3":"A1","4":"A1","5":"A1","6":"A2","7":"A2","8":"A2","9":"B1","10":"A1","11":"B2","12":"A1","13":"A1","14":"A1","15":"A1","16":"A1","17":"A1","18":"A1","19":"A1","20":"A1","21":"A1","22":"A1","23":"A2","24":"A1","25":"A1","26":"A1","27":"A1","28":"A1","29":"A1","30":"A1","31":"A1","32":"A1","33":"A1","34":"B1","35":"B1","36":"A1","37":"B1","38":"B1"},"frequency":{"0":5578,"1":2035,"2":134,"3":1213,"4":1144,"5":103,"6":1372,"7":1845,"8":2593,"9":5835,"10":589,"11":8635,"12":5,"13":3,"14":10,"15":12,"16":18,"17":347,"18":684,"19":1021,"20":1358,"21":1695,"22":2032,"23":2369,"24":2706,"25":542,"26":1622,"27":3786,"28":356,"29":1684,"30":3012,"31":95,"32":2822,"33":5739,"34":3789,"35":2825,"36":13,"37":58,"38":97}}

response = requests.post('http://localhost:5000/uploadinfo', json=json_file)
print(response.text)
"""


print('finished')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
