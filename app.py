from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)
from datetime import datetime

# ROUTES
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/refer')
def refer():
    return render_template('refer.html')

@app.route('/layout')
def header():
    return render_template('layout.html')


@app.route('/header')
def layout():
    return render_template('header.html')


if __name__ == '__main__':
    app.run(debug=True)