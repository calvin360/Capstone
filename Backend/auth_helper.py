'''
Helper functions for auth.py.
Made by Ajay Arudselvam, Calvin Lau
'''
from email.message import EmailMessage
import hashlib
import ssl
# emails from here https://likegeeks.com/python-send-emails/
from smtplib import SMTP
import jwt

from flask import flash
from Database.Data import *
from Backend.error import InputError

SECRET = "Fantastic5"


def hash_password(password):
    '''
    Returns a hashed version of a password

    Arguments:
        password (String) - The password that needs to be hashed

    Exceptions:
        N/A

    Return Value:
        Returns a hashed password
    '''
    hash = hashlib.md5()
    hash.update(password.encode("utf-8"))
    return hash.hexdigest()


def decode_token(token):
    '''
    Returns a decoded token

    Arguments:
        token (String) - The token that needs to bed decoded

    Exceptions:
        N/A

    Return Value:
        Returns a decoded if possible otherwise None
    '''
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception:
        return None


def generate_token(id):
    '''
    Returns a new token based off an id

    Arguments:
        id (int) - The id of a user that needs a token

    Exceptions:
        N/A

    Return Value:
        Returns a decoded if possible otherwise None
    '''
    token = jwt.encode({'id': id}, SECRET, algorithm='HS256')
    return token


def send_mail(reciever, subject, message):
    '''
    Sends emails using SMTP

    Arguments:
        reciever (string) - The email of the recipient\n
        subject  (string) - The subject of the email\n
        message  (string) - The message in the email

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    sender = "foodnation123123@outlook.com"
    password = 'Fantastic5!'
    port = 587
    smtp_server = 'smtp-mail.outlook.com'

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciever

    SSL_context = ssl.create_default_context()

    with SMTP(smtp_server, port) as smtp:
        smtp.starttls(context=SSL_context)
        smtp.login(sender, password)
        smtp.send_message(msg)
        smtp.quit()


def check_pass(numbers, letters, pass1, pass2):
    '''
    Checks if a password is valid

    Arguments:
        numbers (int) - The amount of numbers in the password\n
        letters (int) - The amount of letters in the password\n
        pass1  (string) - The password to be checked\n
        pass2  (string) - The password again to make sure it was entered correctly

    Exceptions:
        InputError - If the password don't match, if the password doesn't have at least\n
                     one number and letter or if password is shorter than 8 characters

    Return Value:
        N/A
    '''
    if pass1 != pass2:
        flash('Passwords do not match', category='error')
        raise InputError(description='Passwords do not match')
    elif numbers < 1 or letters < 1:
        flash('Password must contain atleast 1 letter and 1 number',
              category='error')
        raise InputError(
            description='Password must contain atleast 1 letter and 1 number')
    elif len(pass1) < 8:
        flash('Password must be at least 8 characters', category='error')
        raise InputError(
            description='Password must be at least 8 characters')
    else:
        flash('Password has been changed', category='success')
