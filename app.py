from flask import Flask
from flask import render_template, redirect
from flask import Response, request, jsonify
app = Flask(__name__)
from datetime import datetime

# ROUTES
@app.route('/')
def home():
    return redirect('https://listening-ear.co.uk/')

@app.route('/refer')
def refer():
    return render_template('refer.html')


if __name__ == '__main__':
    app.run(debug=True)