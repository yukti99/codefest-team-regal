from flask import Flask
from flask import render_template, redirect
from flask import Response, request, jsonify, make_response
app = Flask(__name__)
from datetime import datetime
import psycopg2
import json

#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.exc import IntegrityError


conn = psycopg2.connect(database="citus", user="citus", 
                        password="Regal!123", host="c-regal.vbxdxws6j7gzii.postgres.cosmos.azure.com", port="5432") 

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://citus:Regal!123@c-regal.vbxdxws6j7gzii.postgres.cosmos.azure.com/citus' 

#db = SQLAlchemy(app)


ISSUE_TYPES = {
    "bereavement": "bereavement",
    "domestic_abuse": "domestic abuse",
    "divorce_separation": "divorce separation",
    "children_looked_after": "children looked after",
    "suicide_bereavement": "suicide bereavement",
    "depression": "depression",
    "anxiety": "anxiety",
    "stress": "stress",
    "gender_sexuality": "gender sexuality",
    "other": "other"
}

class Client:
    def __init__(self, first_name, last_name, date_of_birth, postal_code, nsh_number, phone_number, address, client_status):
        # self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.postal_code = postal_code
        self.nsh_number = nsh_number
        self.phone_number = phone_number
        self.address = address
        self.client_status = client_status

class ClientIssue:
    def __init__(self, client_id, issue_type, issue_desc, therapist_id, therapist_name, created_date):
        self.client_id = client_id
        self.issue_type = issue_type
        self.issue_desc = issue_desc
        self.therapist_id = therapist_id
        self.therapist_name = therapist_name
        self.created_date = created_date


""" class Client():
    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    postal_code = db.Column(db.String(20))
    nsh_number = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(100))
    client_status = db.Column(db.String(20))

class ClientIssue():
    issue_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    issue_type = db.Column(db.String(50))
    issue_desc = db.Column(db.String(50))
    therapist_id = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    therapist_name = db.Column(db.String(50)) """

curr = conn.cursor()

#jsonfy all the responses

# hard coded data
referrals = {
    1: {
        "first_name": "Sejal",
        "last_name": "Sinha",
        "date_of_birth": "05/02/1999",
        "post_code": "10027",
        "problem_type": ["anxiety", "depression"],
    },
    2: {
        "first_name": "Ashley",
        "last_name": "Anniston",
        "date_of_birth": "05/02/1987",
        "post_code": "07029",
        "problem_type": ["domestic abuse"],
    }
}

# ROUTES
@app.route('/')
def home():
    return redirect('https://listening-ear.co.uk/')

@app.route('/refer', methods =["GET", "POST"])
def refer():
    if request.method == "POST":
        try:
            all_clients = get_all_clients()
            fn = request.form.get("first_name")
            ln = request.form.get("last_name")
            dob = request.form.get("date_of_birth")

            existing_client_id = -1
            existing_client = False
            for c in all_clients:
                c = c[0]
                if str(c["first_name"]).lower() == fn.lower() and str(c["last_name"]).lower() == ln.lower() and c["date_of_birth"] == dob:
                    existing_client_id = c["client_id"]
                    existing_client = True
                    break
            print(f"existing client {existing_client}")

            cur = conn.cursor()
            if not existing_client:
                new_client = Client(
                    first_name=request.form.get('first_name'),
                    last_name=request.form.get('last_name'),
                    date_of_birth=request.form.get('date_of_birth'),
                    postal_code=request.form.get('zipcode'),
                    nsh_number=request.form.get('nsh'),
                    phone_number=request.form.get('phone'),
                    address= request.form.get('address_line1') + ' ' + request.form.get('address_line2') + ' ' + request.form.get('city') + \
                ' '+ request.form.get('state') + request.form.get('zipcode'),
                    client_status="Inactive"
                )
                        
                insert_query = """
                INSERT INTO clients (first_name, last_name, date_of_birth, postal_code, nsh_number, phone_number, address, client_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING client_id
                """
                cur.execute(insert_query, (new_client.first_name, new_client.last_name, new_client.date_of_birth, new_client.postal_code, 
                                        new_client.nsh_number, new_client.phone_number, new_client.address, new_client.client_status))
                conn.commit()
                new_client_record = cur.fetchone()
                existing_client_id = int(new_client_record[0])

            issue_type = ""
            if request.form.get("bereavement"):
                issue_type += "bereavement,"
            if request.form.get("domestic_abuse"):
                issue_type += "domestic_abuse,"
            if request.form.get("children_looked_after"):
                issue_type += "children_looked_after,"
            if request.form.get("suicide_bereavement"):
                issue_type += "suicide_bereavement,"
            if request.form.get("depression"):
                issue_type += "depression,"
            if request.form.get("anxiety"):
                issue_type += "anxiety,"
            if request.form.get("stress"):
                issue_type += "stress,"
            if request.form.get("gender_sexuality"):
                issue_type += "gender_sexuality,"
            if request.form.get("other"):
                issue_type += "other,"    

            issue_type_cons = issue_type[:-1]
                    
            new_client_issue = ClientIssue(
                client_id=existing_client_id,
                issue_type = issue_type_cons,
                issue_desc = issue_type_cons,
                therapist_id=-1,
                therapist_name="",
                created_date=datetime.now().strftime("%Y-%m-%d")
            )

            insert_client_issue_query = """
             INSERT INTO client_issues (client_id, issue_type, issue_desc, therapist_id, created_date, therapist_name)
             VALUES (%s, %s, %s, %s, %s, %s)
            """
            print(insert_client_issue_query)
          
            cur.execute(insert_client_issue_query, (new_client_issue.client_id, new_client_issue.issue_type, new_client_issue.issue_desc,
                                                    new_client_issue.therapist_id, new_client_issue.created_date, 
                                                    new_client_issue.therapist_name))
            conn.commit()
            # return jsonify(message="Client issue inserted successfully")
        except Exception as e:
            print(e)
            return jsonify(error="Failed to insert client issue"), 400
    return render_template('refer.html')

# @app.route('/admin')
# def admin():
#     curr.execute('''select row_to_json(clients) from clients''')
#     result = curr.fetchall()
#     curr.close
#     referrals = []
#     for row in result:
#         referrals.append(row[0])
#     return render_template('admin.html', referrals = referrals)

@app.route('/admin')
def admin():
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
    return render_template('admin.html', referrals = return_resp)

# @app.route('/view_referral/<id>')
# def view_referral(id):
#     cur = conn.cursor()
#     curr.execute(f"select row_to_json(clients) from clients where client_id = {id}")
#     result = curr.fetchall()
#     curr.close
#     clients = []
#     for row in result:
#         clients.append(row[0])
#     print(clients[0])
#     return render_template('view_referral.html', client_id=id, client_dict=clients[0]) 

@app.route('/view_referral/<id>')
def view_referral(id):
    cur = conn.cursor()
    curr.execute(f"select row_to_json(a) from (select * from clients where client_id = {id}) a")
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
    return render_template('view_referral.html', client_id=id, client_dict=return_resp[0]) 

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

def get_all_clients():
    cur = conn.cursor()
    curr.execute('''select row_to_json(a) from ( \
                 select * from clients
                ) a''')
    result = curr.fetchall()
    curr.close
    return result

#Add new client
# @app.route('/add_client', methods=['POST'])
def insert_client():
    if request.method == 'POST':
        try:
            all_clients = get_all_clients()
            fn = request.form.get("first_name")
            ln = request.form.get("last_name")
            dob = request.form.get("date_of_birth")

            existing_client_id = -1
            existing_client = False
            for c in all_clients:
                c = c[0]
                if str(c["first_name"]).lower() == fn.lower() and str(c["last_name"]).lower() == ln.lower() and c["date_of_birth"] == dob:
                    existing_client_id = c["client_id"]
                    existing_client = True
                    break
            print(f"existing client {existing_client}")

            cur = conn.cursor()
            if not existing_client:
                new_client = Client(
                    first_name=request.form.get('first_name'),
                    last_name=request.form.get('last_name'),
                    date_of_birth=request.form.get('date_of_birth'),
                    postal_code=request.form.get('zipcode'),
                    nsh_number=request.form.get('nsh'),
                    phone_number=request.form.get('phone'),
                    address= request.form.get('address_line1') + ' ' + request.form.get('address_line2') + ' ' + request.form.get('city') + \
                ' '+ request.form.get('state') + request.form.get('zipcode'),
                    client_status="Inactive"
                )
                        
                insert_query = """
                INSERT INTO clients (first_name, last_name, date_of_birth, postal_code, nsh_number, phone_number, address, client_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING client_id
                """
                cur.execute(insert_query, (new_client.first_name, new_client.last_name, new_client.date_of_birth, new_client.postal_code, 
                                        new_client.nsh_number, new_client.phone_number, new_client.address, new_client.client_status))
                conn.commit()
                new_client_record = cur.fetchone()
                existing_client_id = int(new_client_record[0])

            issue_type = ""
            if request.form.get("bereavement"):
                issue_type += "bereavement,"
            if request.form.get("domestic_abuse"):
                issue_type += "domestic_abuse,"
            if request.form.get("children_looked_after"):
                issue_type += "children_looked_after,"
            if request.form.get("suicide_bereavement"):
                issue_type += "suicide_bereavement,"
            if request.form.get("depression"):
                issue_type += "depression,"
            if request.form.get("anxiety"):
                issue_type += "anxiety,"
            if request.form.get("stress"):
                issue_type += "stress,"
            if request.form.get("gender_sexuality"):
                issue_type += "gender_sexuality,"
            if request.form.get("other"):
                issue_type += "other,"    

            issue_type_cons = issue_type[:-1]
                    
            new_client_issue = ClientIssue(
                client_id=existing_client_id,
                issue_type = issue_type_cons,
                issue_desc = issue_type_cons,
                therapist_id=-1,
                therapist_name="",
                created_date=datetime.now().strftime("%Y-%m-%d")
            )

            insert_client_issue_query = """
             INSERT INTO client_issues (client_id, issue_type, issue_desc, therapist_id, created_date, therapist_name)
             VALUES (%s, %s, %s, %s, %s, %s)
            """
            print(insert_client_issue_query)
          
            cur.execute(insert_client_issue_query, (new_client_issue.client_id, new_client_issue.issue_type, new_client_issue.issue_desc,
                                                    new_client_issue.therapist_id, new_client_issue.created_date, 
                                                    new_client_issue.therapist_name))
            conn.commit()
            # return jsonify(message="Client issue inserted successfully")
        except Exception as e:
            print(e)
            return jsonify(error="Failed to insert client issue"), 400
    



if __name__ == '__main__':
    app.run(debug=True)