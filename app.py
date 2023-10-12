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

@app.route('/testdb')
def test_db():
    curr.execute('''select row_to_json(clients) from clients''')
    result = curr.fetchall()
    curr.close
    referrals = []
    for row in result:
        referrals.append(row[0])
    return make_response(jsonify(referrals),'application/json')

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
    return render_template('refer.html')

@app.route('/refer')
def refer():
    return render_template('refer.html')

@app.route('/test')
def test():
    return render_template('example.html')

@app.route('/admin')
def admin():
    curr.execute('''select row_to_json(clients) from clients''')
    result = curr.fetchall()
    curr.close
    referrals = []
    for row in result:
        referrals.append(row[0])
    return render_template('admin.html', referrals = referrals)

@app.route('/view_referral/<id>')
def view_referral(id):
    cur = conn.cursor()
    curr.execute(f"select row_to_json(clients) from clients where client_id = {id}")
    result = curr.fetchall()
    curr.close
    clients = []
    for row in result:
        clients.append(row[0])
    print(clients[0])
    return render_template('view_referral.html', client_id=id, client_dict=clients[0]) 

if __name__ == '__main__':
    app.run(debug=True)