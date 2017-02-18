import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def sleep():
    time.sleep(1)
    return jsonify({})

app.run(debug=True)
