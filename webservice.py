#6D/19090125/Ramdon Baehaki Nur Faiz
#6D/19098001/Saksono Bayu Ajie Sumantri

from flask import Flask, jsonify, request,make_response
import os, random, string
from flask_sqlalchemy import SQLAlchemy
from chat import get_response

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    token = db.Column(db.String(225), unique=True, nullable=True)

class chat(db.Model):
    message = db.Column(db.String(225), unique=False, nullable=False)
    answer = db.Column(db.String(225), unique=False, nullable=False)
db.create_all()

@app.route('/api/register', methods=['POST'])
def daftar():
    dataUsername = request.json['username']
    dataPassword = request.json['password']
    
    if dataUsername and dataPassword:
        dataModel = User(username=dataUsername, password=dataPassword)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"Msg ":"Register Berhasil"}), 200)
    return jsonify({"Msg ":"Username/Password harus diisi"})

@app.route('/api/v1/login', methods=['POST'])
def masuk():
    dataUsername = request.json['username']
    dataPassword = request.json['password']
    akun = User.query.filter_by(username=dataUsername, password=dataPassword).first()
    if akun:
        dataToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
        User.query.filter_by(username=dataUsername, password=dataPassword).update({'token': dataToken})
        db.session.commit()
        return make_response(jsonify({"Token Anda":dataToken}),200)
    return jsonify({"msg":"Mengambil Info Token Gagal"}) 

@app.post("/predict")
def predict():
    token = request.json['token']
    text = request.get_json().get("message")
    response = get_response(text)
    username=User.query.filter_by(token=token).first()
    if username:
        dataModel = chat(message=text, answer=response)
        db.session.add(dataModel)
        db.session.commit()
    return {"answer": response}
        
if __name__ == '__main__':
    app.run(debug=True, port=4000)
