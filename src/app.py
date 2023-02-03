"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
member__1 = { "id" : jackson_family._generateId(),
            "firstname" :"John", 
            "lastname": jackson_family.last_name,
            "age" : 33, 
            "luckyNumbers": [7, 13, 22]}
member_2 = { "id" : jackson_family._generateId(),
            "firstname" :"Jane", 
            "lastname": jackson_family.last_name,
            "age" : 35, 
            "luckyNumbers": [10, 14, 3]}
member_3 = { "id" : jackson_family._generateId(),
            "firstname" :"Jimmy", 
            "lastname": jackson_family.last_name,
            "age" : 5, 
            "luckyNumbers": [1]}
jackson_family.add_member(member_1)
jackson_family.add_member(member_2)
jackson_family.add_member(member_3)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members


    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def handle_member():

    members = request.json

    id = members["id"]
    first_name = members["first_name"]
    last_name = members["last_name"]
    age = members["age"]
    lucky_numbers = members["lucky_numbers"]

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_memberIn(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200 

@app.route('/deletemember/<int:id>', methods=['DELETE'])
def handle_delete(id):
    jackson_family.delete_member(id)
    return jsonify(member), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
