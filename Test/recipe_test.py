from datetime import datetime
from urllib import request, response
import pytest
import requests
import json


port = 5123
url = f"http://localhost:{port}/"


def test_add_recipe():
    response = requests.post(
        url+'register', json={"firstName": 'first', "lastName": 'second', "username": 'name', "password": 'password1', "password2": 'password1', "email": 'abc@agmail.com'})
    assert response.status_code == 400
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    assert response1.status_code == 200

    rec = requests.post(
        url+'add/recipe', json={"recipe_name": 'chicken', "email": 'abc@agmail.com', "recipe_ingredients": 'chicken 100g, salt, onion 200g, \n pepper',
                                "recipe_method": 'cook chicken :)', "recipe_description": 'yummy chicken'})
    assert rec.status_code == 200
    assert rec.json()['recipe_id'] == 1
    assert rec.json()['recipe_name'] == 'chicken'
    assert rec.json()['recipe_method'] == 'cook chicken :)'
    assert rec.json()[
        'recipe_ingredients'] == 'chicken 100g, salt, onion 200g, \n pepper'
    assert rec.json()['recipe_description'] == 'yummy chicken'
    assert rec.json()['email'] == 'abc@agmail.com'
    assert rec.json()['recipeLikes'] == 0
    assert rec.json()['recipeDislikes'] == 0


def test_remove_recipe():
    response = requests.post(
        url+'register', json={"firstName": 'first', "lastName": 'second', "username": 'name', "password": 'password1', "password2": 'password1', "email": 'abc@agmail.com'})
    assert response.status_code == 400
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    assert response1.status_code == 200

    rec = requests.post(
        url+'add/recipe', json={"recipe_name": 'chicken', "email": 'abc@agmail.com', "recipe_ingredients": 'chicken 100g, salt, onion 200g, \n pepper',
                                "recipe_method": 'cook chicken :)', "recipe_description": 'yummy chicken'})
    assert rec.status_code == 200

    remove = requests.post(url+'remove/recipe',
                           json={"id": '1', "email": 'abc@agmail.com'})
    assert remove.status_code == 200

    remove = requests.get(url+'get/recipe',
                          json={"id": '1'})
    assert remove.status_code == 400


def test_edit_recipe():
    response = requests.post(
        url+'register', json={"firstName": 'first', "lastName": 'second', "username": 'name', "password": 'password1', "password2": 'password1', "email": 'abc@agmail.com'})
    assert response.status_code == 400
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    assert response1.status_code == 200

    time_a = datetime.now()

    rec = requests.post(
        url+'add/recipe', json={"recipe_name": 'chicken', "email": 'abc@agmail.com', "recipe_ingredients": 'chicken 100g, salt, onion 200g, \n pepper',
                                "recipe_method": 'cook chicken :)', "recipe_description": 'yummy chicken'})
    assert rec.status_code == 200
    assert rec.json()['recipe_id'] == 3
    assert rec.json()['recipe_name'] == 'chicken'
    assert rec.json()['recipe_method'] == 'cook chicken :)'
    assert rec.json()[
        'recipe_ingredients'] == 'chicken 100g, salt, onion 200g, \n pepper'
    assert rec.json()['recipe_description'] == 'yummy chicken'
    assert rec.json()['email'] == 'abc@agmail.com'
    assert rec.json()['recipeLikes'] == 0
    assert rec.json()['recipeDislikes'] == 0
    # print(type(datetime.strptime(
    #     rec.json()['recipe_created_time'], '%Y-%m-%d %H:%M:%S.%f')))
    # assert (
    #     abs(time_a - datetime.strptime(rec.json()['recipe_created_time'], '%Y-%m-%d %H:%M:%S.%f')) < 2)

    # time_b = datetime.now()

    edit = requests.post(
        url+'edit/recipe', json={"recipe_id": rec.json()['recipe_id'], "email": 'abc@agmail.com', "recipe_name": 'chicken dinner',  "recipe_ingredients": 'winner 1, chicken 100g, salt, onion 200g, \n pepper',
                                 "recipe_method": 'win chicken', "recipe_description": 'yummy winner chicken'})
    assert edit.status_code == 200
    assert edit.json()['recipe_id'] == rec.json()['recipe_id']
    assert edit.json()['recipe_name'] == 'chicken dinner'
    assert edit.json()['recipe_method'] == 'win chicken'
    assert edit.json()[
        'recipe_ingredients'] == 'winner 1, chicken 100g, salt, onion 200g, \n pepper'
    assert edit.json()['recipe_description'] == 'yummy winner chicken'
    assert edit.json()['email'] == 'abc@agmail.com'
    assert edit.json()['recipeLikes'] == 0
    assert edit.json()['recipeDislikes'] == 0
    # assert (abs(time_b-datetime(edit.json()['recipe_created_time'])) < 2)
