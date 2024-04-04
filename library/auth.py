from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from .models import User
from datetime import datetime
from . import db
auth = Blueprint('auth', __name__)


#SIGNUP
@auth.route('/signup', methods=['POST'])
def signup():
    req = request.json
    email = req['email']
    name = req['name']
    password = req['password']
    role = req['role']
    time = datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    user = User.query.filter_by(email=email).first()
    if user:
        return make_response(jsonify({"account":"exists"}), 401)
    new_user = User(email=email, name=name, isAdmin=role , password=password, last_visited=formatted_time)
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({"email":email, "name": name}), 200)

#LOGIN
@auth.route('/login', methods=['POST'])
def login():
    req = request.json
    email = req["email"]
    password = req["password"]
    role = req["role"]

    user = User.query.filter_by(email=email).first()
    wrong_pass = {"password": "INVALID CREDENTIALS"}
    user_response = {"email": user.email, "name": user.name, "userid": user.id, "role": user.role}

    if not user or password != user.password or user.role != role:
        return make_response(jsonify(wrong_pass), 401)

    return make_response(jsonify(user_response), 200)

#LOGOUT
@auth.route('/logout', methods=['POST'])
def logout():
    return make_response(jsonify({"user": "logged out"}), 200)