from urllib import request, response
import pytest
import requests
import json


port = 5123
url = f"http://localhost:{port}/"


def test_register_valid():
    response = requests.post(
        url+'register', json={"firstName": 'first', "lastName": 'second', "username": 'name', "password": 'password1', "password2": 'password1', "email": 'abc@agmail.com'})
    assert response.status_code == 400
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    assert response1.status_code == 200
    initresp = requests.post(
        url+'deleteAccount', json={"token": response1.json()['token'], "password": 'password1'})
    assert initresp.status_code == 200
    response = requests.post(
        url+'register', json={"firstName": 'first', "lastName": 'second', "username": 'name', "password": 'password1', "password2": 'password1', "email": 'abc@agmail.com'})
    assert response.status_code == 200
    assert response.json()['email'] == 'abc@agmail.com'
    assert response.json()['firstName'] == 'first'
    assert response.json()['lastName'] == 'second'


def test_login_valid():
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    assert response1.status_code == 200
    assert response1.json()['id'] == 1


def test_login_invalid_password():
    response1 = requests.post(
        url+'login', json={"password": 'password121', "email": 'abc@agmail.com'})
    assert response1.status_code == 400
    #assert response1.json()['error'] == "Entered Password is Incorrect"


def test_login_invalid_email():
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abcd@agmail.com'})
    assert response1.status_code == 400
    #assert response1.json()['error'] == "Entered Email is Incorrect"


def test_logout_invaild_email():
    response1 = requests.post(
        url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
    response1 = requests.post(
        url+'logout', json={"token": response1.json()['token']})
    assert response1.status_code == 200
    assert response1.json()['success'] == "User has been logged off !"


# def test_logout_but_not_logged_in():
#     response1 = requests.post(
#         url+'login', json={"password": 'password1', "email": 'abc@agmail.com'})
#     response1 = requests.post(
#         url+'logout', json={"token": response1.json()['token']})

#     assert response1.status_code == 200
#     assert response1.json()['error'] == "User not found !"
