from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, make_response
app = Flask(__name__)
from datetime import datetime
import psycopg2
import json

conn = psycopg2.connect(database="citus", user="citus", 
                        password="Regal!123", host="c-regal.vbxdxws6j7gzii.postgres.cosmos.azure.com", port="5432") 

curr = conn.cursor()

#jsonfy all the responses

@app.route('/testdb')
def test_db():
    curr.execute('''select row_to_json(clients) from clients''')
    result = curr.fetchall()
    curr.close
    return_resp = []
    for row in result:
        return_resp.append(row[0])
    #print(",".join(return_resp))    
        #return_resp.append(row)
    return make_response(jsonify(return_resp),'application/json')


@app.route('/')
def index():
    return "Hello World"


@app.route('/testdb/save', methods=['POST'])
def testdb_save():
    #cli_id = request.form.get('client_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    dob = request.form.get('date_of_birth')
    depart = request.form.get('department')

    # Insert the data into the database
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (first_name, last_name,date_of_birth, department) VALUES (%s, %s, %s, %s)", (first_name, last_name, dob, depart))
    conn.commit()
 
    return 'User created successfully!'


#get all clients
@app.route('/getclients/')
def get_clients():
    cur = conn.cursor()
    curr.execute('''select row_to_json(a) from ( \
                 select clients.*, client_issues.* from clients left join \
                 client_issues on \
                 clients.client_id = client_issues.client_id \
                ) a''')
    result = curr.fetchall()
    curr.close
    return_resp = []
    for row in result:
        return_resp.append(row[0])
    return make_response(jsonify(return_resp),'application/json')


#Add new client

#Update existing client

#schedule appointment 

#



if __name__ == '__main__':
    app.run(debug=True)