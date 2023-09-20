from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB instance

client = MongoClient('mongodb://34.79.240.29:27017/')
db = client['urls']
collection = db['urls']

@app.route('/')
def index():
    # Retrieve the list of URLs from MongoDB
    urls = [doc["url"] for doc in collection.find()]

    # Render the HTML template with the URLs
    return render_template('index.html', headline='List of Serials', urls=urls)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
