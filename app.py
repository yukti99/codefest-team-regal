from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, make_response
app = Flask(__name__)
from datetime import datetime
import psycopg2
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError



conn = psycopg2.connect(database="citus", user="citus", 
                        password="Regal!123", host="c-regal.vbxdxws6j7gzii.postgres.cosmos.azure.com", port="5432") 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://citus:Regal!123@c-regal.vbxdxws6j7gzii.postgres.cosmos.azure.com/citus' 

db = SQLAlchemy(app)

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    postal_code = db.Column(db.String(20))
    nsh_number = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(100))
    client_status = db.Column(db.String(20))

class ClientIssue(db.Model):
    issue_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    issue_type = db.Column(db.String(50))
    issue_desc = db.Column(db.String(50))
    therapist_id = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    therapist_name = db.Column(db.String(50))

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
                 select * from clients
                ) a''')
    result = curr.fetchall()
    curr.close
    return_resp = []
    client_issues = get_issues()
    for client in result:
        c = client[0]
        issues_array = []
        for issues in client_issues:
            iss = issues[0]
            if iss["client_id"] == c["client_id"]:
                issues_array.append(iss)
        c["issues"] = issues_array
        return_resp.append(c)
    print(return_resp)
    return make_response(jsonify(return_resp),'application/json')

def get_issues():
    cur = conn.cursor()
    curr.execute('''select row_to_json(a) from ( \
                 select * from client_issues
                ) a''')
    result = curr.fetchall()
    curr.close
    return result

#Add new client
@app.route('/add_client', methods=['POST'])
def insert_client():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_client = Client(
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=data['date_of_birth'],
                postal_code=data['postal_code'],
                nsh_number=data['nsh_number'],
                phone_number=data['phone_number'],
                address=data['address'],
                client_status=data['client_status'])
            
            db.session.add(new_client)
            db.session.flush()
            db.session.commit()
            new_client_issue = ClientIssue(
                client_id=new_client.client_id,
                issue_type=data['issue_type'],
                issue_desc=data['issue_desc'],
                therapist_id=data['therapist_id'],
                created_date=data['created_date']
            )
            db.session.add(new_client_issue)
            db.session.commit()  
            return jsonify(message="Client inserted successfully")
        except IntegrityError as e:
            db.session.rollback()
            return jsonify(error="Failed to insert client issue"), 400
    

#Update existing client

#schedule appointment 




if __name__ == '__main__':
    app.run(debug=True)