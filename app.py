from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)
from datetime import datetime

@app.route('/')
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)