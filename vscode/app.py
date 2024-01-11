from flask import Flask
from testIndex import testIndex_bp

app = Flask(__name__)
app.register_blueprint(testIndex_bp)

@app.route("/")
def inedx():
    return "index is here"

if __name__ =="__main__":
    app.run(debug=True)