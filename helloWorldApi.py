from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/hello")
def hello_hello():
    return "<p>Hello, Hello!</p>"

if __name__ == '__main__': 
    app.run(debug=True)