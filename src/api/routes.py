"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/hello2', methods=['POST', 'GET'])
def hello2():
    response_body = {
        "message": "Hello!3"
    }
    return jsonify(response_body), 200

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Could not find email"}), 401

    if password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@api.route("/signup", methods=["POST"])
def signup():
    body = request.get_json()

    user = User.query.filter_by(email=body["email"]).first()
    if user is not None:
        return jsonify({"msg": "Ya se encuentra un usuario creado con ese correo"}), 409

    new_user = User(
        email=body["email"],
        password=body["password"],  # En producción, se recomienda encriptar la contraseña
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "Usuario creado"
    }
    return jsonify(response_body), 201
