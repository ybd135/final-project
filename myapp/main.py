from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB instance

client = MongoClient('mongodb://34.79.240.29:27017/')

db = client['ybd135']
collection = db['urls']
add_password = "1234"


@app.route('/', methods=['GET', 'POST'])
def index():
    urls = list(collection.find())  # Retrieve all key-value pairs from MongoDB
    return render_template('index.html', urls=urls)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
