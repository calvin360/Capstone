from os import pardir
from sqlalchemy.sql.functions import user
from .Data import *
from . import db
from Backend.auth import *
from Backend.recipe import check_recipe

from flask import Blueprint, jsonify, request, flash,  Flask, redirect, url_for, render_template, session, redirect, url_for, g
import json
from sqlalchemy import desc
from telnetlib import STATUS
from werkzeug.utils import secure_filename
import os
import fnmatch
from flask import current_app

apps = Blueprint('apps', __name__)


@apps.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@apps.before_request
def before_request():
    g.user = None
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        g.user = user


@apps.route("/")
def home():
    recipes = Recipe.query.all()
    return render_template("index.html", recipes=recipes)


@apps.route('/login', methods=['POST'])
def appLogin():
    data = request.get_json()

    result = login(data['email'], data['password'])
    if ('error' in result):
        return jsonify(result)

    return result
    # user = get_user_id(result['id'])
    # user['token'] = result['token']


@apps.route('/register', methods=['POST'])
def appRegister():
    # db.drop_all()
    # print(db)
    data = request.get_json()
    # print(data['username'])
    return jsonify(register(data['firstName'], data['lastName'], data['password'], data['email'], data['username'], data['password2']))


@apps.route('/deleteAccount', methods=['POST'])
def appDeleteAccount():
    data = request.get_json()
    return jsonify(deleteAccount(data['token'], data['password']))


@apps. route('/logout', methods=(['POST']))
def appLogout():
    data = request.get_json()
    result = logout(data['token'])
    return jsonify(result)


@apps.route('/request/password/reset', methods=['POST'])
def reset_req():
    data = request.get_json()
    email = data['email']
    return jsonify(request_password_reset(email))


@apps.route('/reset/password', methods=['POST'])
def reset_pass():
    data = request.get_json()
    token = data['token']
    code = data['code']
    password = data['password']
    return jsonify(reset_password(token, code, password))


@apps.route('/add/recipe', methods=['POST'])
def add_recipe_web():
    data = request.get_json()
    email = data['email']
    recipe_name = data['recipe_name']
    recipe_ingredients = data['recipe_ingredients']
    recipe_method = data['recipe_method']
    recipe_description = data['recipe_description']
    return jsonify(add_recipe(recipe_name, email, recipe_ingredients, recipe_method, recipe_description))


@apps.route('/edit/recipe', methods=['POST'])
def edit_recipe_web():
    data = request.get_json()
    email = data['email']
    id = data['recipe_id']
    recipe_name = data['recipe_name']
    recipe_ingredients = data['recipe_ingredients']
    recipe_method = data['recipe_method']
    recipe_description = data['recipe_description']
    return jsonify(edit_recipe(id, email, recipe_name, recipe_ingredients, recipe_method, recipe_description))


@apps.route('/remove/recipe', methods=['POST'])
def remove_recipe_web():
    data = request.get_json()
    id = int(data['id'])
    email = data['email']
    return jsonify(remove_recipe(id, email))


@apps.route('/get/recipe', methods=['GET'])
def get_recipe_web():
    data = request.get_json()
    id = int(data['id'])
    return jsonify(get_recipe(id))
