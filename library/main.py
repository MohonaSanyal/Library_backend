from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
main = Blueprint('main', __name__)

@main.route('/')
def index():
    status = {"Status": "Active"}  
    return make_response(jsonify(status), 200)