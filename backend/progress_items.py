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


# Requires nothing
@app.route('/progress', methods=['GET', 'POST'])
def progress():
    propgress_items = pd.read_sql('progress_items2', engine)
    propgress_items = propgress_items.to_json()

    return propgress_items



"""
#FRONTEND
import requests
import pandas as pd

response = requests.post('http://localhost:5000/progress')
print(response.text)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




