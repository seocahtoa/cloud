from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.run(debug=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# @app.route('/')
def hello_world():
    return 'This is my first API call!'

# @app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)

# @app.route('/user')
def get_user():
    print("User is: ")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

