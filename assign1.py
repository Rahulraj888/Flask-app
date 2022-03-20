from flask import Flask

import redis

#import hashlib

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/User"

mongo = PyMongo(app)

r = redis.Redis(host="127.0.0.1",port = 6379)

#status = r.ping()

@app.route('/add',methods=['POST'])

def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':

        _hashed_password = generate_password_hash(_password)

        id = mongo.db.Employeedb.insert({'name':_name,'email':_email,'pwd':_hashed_password})
        
        resp = jsonify("user added successfully")

        resp.status_code = 200

        return resp
    
    else:
        return not_found()

@app.route('/users')
def users():
    users = mongo.db.Employeedb.find()
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.db.Employeedb.find_one({'_id' : ObjectId(id)})
    resp = dumps(user)
    return resp
        

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.Employeedb.delete_one({'_id':ObjectId(id)})
    resp = jsonify("user deleted successfully")

    resp.status_code = 200

    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'PUT':

        _hashed_password = generate_password_hash(_password)

        mongo.db.Employeedb.update_one({'_id' : ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set' : {'name' : _name, 'email':_email,'pwd':_hashed_password}})
        resp =jsonify("user updated succssfully")

        resp.status_code=200
        return resp
    
    else:
        return not_found()



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message':'Not Found' + request.url 
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True)

