from flask import Flask
from flask import render_template, redirect
from flask import Response, request, jsonify
app = Flask(__name__)
from datetime import datetime

# ROUTES
@app.route('/')
def home():
    return redirect('https://listening-ear.co.uk/')

@app.route('/refer', methods =["GET", "POST"])
def refer():
    if request.method == "POST":
       first_name = request.form.get("first-name")
       last_name = request.form.get("last-name") 
       issues = request.form.get("bereavement") != None
       print(f"Your name is {first_name} {last_name}")
       print(f"Does client have bereavement issue: {issues}")
    return render_template('refer.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)