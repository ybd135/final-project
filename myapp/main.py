from flask import Flask, render_template

app = Flask(__name__)

# Sample list of URLs (you can replace this with your own list)
urls = [
    "https://www.example.com",
    "https://www.google.com",
    "https://www.github.com",
]

@app.route("/")
def index():
    # Render the HTML template and pass the list of URLs to it
    return render_template("index.html", urls=urls)

if __name__ == "__main__":
    app.run(debug=True)