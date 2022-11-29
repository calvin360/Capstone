'''
Functions for handling user authorisation and general account management.
Made by Ajay Arudselvam, Calvin Lau and Keerthivasan Gopalraj
'''
import re
import random

from string import ascii_letters, digits
from flask import flash
from Database.Data import *
from Backend.auth_helper import *
from Backend.helper import *
from Backend.error import InputError

VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"


def login(email, password):
    '''
    logs in a a user using the given email and password

    Arguments:
        email    (string) - The user's email address\n
        password (string) - The user's password

    Exceptions:
        InputError - If the provided email isn't in the database,
                    if the email is not in the correct format\n
                     or if the password is incorrect

    Return Value:
        Returns a dictionary with the user id and user token
    '''
    if not re.search(VALID_EMAIL, email):
        flash('Email is not valid', category='error')
        raise InputError(description='Invalid email format')
    elif not exists_email(email):
        flash('Email or password is invalid', category='error')
        raise InputError(
            description='Email or password is invalid')
    else:
        user = User.query.filter_by(email=email).first()
        if user.password != hash_password(password):
            flash('Email or password is invalid', category='error')
            raise InputError(description='Email or password is invalid')
        else:
            token = generate_token(user.id)
            add_token(user, token)
            flash('Successful Login', category='success')
            return {'id': user.id, 'token': token}


def register(firstName, lastName, password, email, username, password_2):
    '''
    registers a first time user using the given fields

    Arguments:
        firstName (string) - The user's first name\n
        lastName  (string) - The user's last name\n
        password  (string) - The user's password\n
        email     (string) - The user's email address\n
        username  (string) - The display name for the user\n
        password2 (string) - The user's password entered again to check that
        the password was entered correctly

    Exceptions:
        InputError - If the provided email isn't in the database, if the email is
                     not in the correct format,if the email is not the correct length,\n
                     if a first and last name isn't provided, if the name is longer than 100\n
                     characters, if the password isn't at least 8 characters long and contains at\n
                     least 1 number and 1 letter, if the password is longer than 100 characters, \n
                     if the passwords don't match or if the username is already taken\n

    Return Value:
        Returns a dictionary with the user id and user token
    '''
    numbers = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    if not re.search(VALID_EMAIL, email):
        flash('Email is not valid', category='error')
        raise InputError(description='Email is not valid')
    elif exists_email(email):
        flash('Email has already been registerd', category='error')
        raise InputError(description='Email already registerd')
    elif len(email) < 4:
        flash('Email must be greater than 4 characters', category='error')
        raise InputError(description='Email must be greater than 4 characters')
    elif len(email) > 100:
        flash('Email must be less than 100 characters', category='error')
        raise InputError(description='Email must be less than 100 characters')
    elif len(firstName) <= 0:
        flash('Must enter first name', category='error')
        raise InputError(description='Must enter first name')
    elif len(firstName) > 100:
        flash('First name must be less than 100 characters', category='error')
        raise InputError(
            description='First name must be less than 100 characters')
    elif len(lastName) <= 0:
        flash('Must enter last name', category='error')
        raise InputError(description='Must enter last name')
    elif len(lastName) > 100:
        flash('Last name must be less than 100 characters', category='error')
        raise InputError(
            description='Last name must be less than 100 characters')
    elif len(password) < 8:
        flash('Password must be at least 8 characters', category='error')
        raise InputError(description='Password must be at least 8 characters')
    elif len(password) > 100:
        flash('Password must be less than 100 characters', category='error')
        raise InputError(
            description='Password must be less than 100 characters')
    elif numbers < 1 or letters < 1:
        flash('Password must contain atleast 1 letter and 1 number', category='error')
        raise InputError(
            description='Password must contain atleast 1 letter and 1 number')
    elif password != password_2:
        flash('Passwords must match', category='error')
        raise InputError(description='Password must match')
    elif username_exists(username):
        flash('username has already been registerd', category='error')
        raise InputError(description='Username already registerd')
    else:
        hash = hash_password(password)
        user = add_user(firstName, lastName, hash, email, username)
        log = login(email, password)
        user = get_user_email(email)
        user['token'] = log['token']
        return user


def deleteAccount(token, password):
    '''
    deletes an account from the database

    Arguments:
        token    (string) - The user's token\n
        password (string) - The user's password

    Exceptions:
        InputError - If the token is invalid, if the password is incorrect or if the user can't be found

    Return Value:
        N/A
    '''
    u = decode_token(token)
    user = User.query.filter_by(id=u['id']).first()
    if not exists_token(user.id):
        flash('Token Invalid', category='error')
        raise InputError(description='Token Invalid')
    if user:
        if user.password != hash_password(password):
            flash('Password is incorrect', category='error')
            raise InputError(description='Password is incorrect')
        else:
            remove_user(user.email)
            flash('Account Deleted', category='success')
            return {'success': 'Account has been deleted'}
    else:
        flash('Cannot delete account', category='error')
        raise InputError(description='Cannot delete account')


def logout(token):
    '''
    deletes an account from the database

    Arguments:
        token    (string) - The user's token\n
        password (string) - The user's password

    Exceptions:
        InputError - If the token is invalid, if the password is incorrect or if the user can't be found

    Return Value:
        N/A
    '''
    u = decode_token(token)
    user = User.query.filter_by(id=u['id']).first()
    if user:
        if exists_token(user.id):
            user.token = None
            db.session.commit()
            flash('Successful Logout', category='success')
            return {'success': 'User has been logged off !'}
        return {'error': 'Token Invalid !'}
    else:
        return {'error': 'User not found !'}


def request_password_reset(email):
    '''
    request_password_reset allows users to request a one use password reset code to be sent to their registered email

    Arguments:
        email (string) - The user's email address

    Exceptions:
        InputError - If the provided email isn't in the database

    Return Value:
        N/A
    '''
    if not exists_email(email):
        flash('Email does not exist', category='error')
        raise InputError(description='Invalid email address')

    user = User.query.filter_by(email=email).first()
    code = ''.join(random.choice(ascii_letters+digits)for i in range(6))
    msg = 'Lost your password? Good one! Here\'s your code: ' + code
    send_mail(email, 'Food Nation Password Reset', msg)
    add_reset_code(user.id, code)

    if user.token is not None:
        logout(user.token)


def reset_password(email, token, code, new_password, new_password1):
    '''
    request_password allows users to reset their password using a one use password reset code

    Arguments:
        token (string)        - The token representing the user trying to call the function\n
        code (string)         - The user's one use password reset code\n
        new_password (string) - The user's new password

    Exceptions:
        InputError  - If the provided password is too short or the reset code is incorrect

    Return Value:
        N/A
    '''
    u = decode_token(token)
    if u is not None:
        user = User.query.filter_by(id=u['id']).first()
    else:
        user = User.query.filter_by(email=email).first()

    if user is None:
        flash('Email does not exist', category='error')
        raise InputError(description='Invalid email address')
    # logout if logged in
    if user.token is not None:
        logout(user.token)
    if user.reset_code != code:
        flash('Incorrect reset code', category='error')
        raise InputError(description='Wrong reset code')

    numbers = sum(c.isdigit() for c in new_password)
    letters = sum(c.isalpha() for c in new_password)
    check_pass(numbers, letters, new_password, new_password1)
    change_password(user.email, new_password)
    add_reset_code(user.id, None)
    return


def change_password_request(email, oldpass, pass1, pass2):
    '''
    Changes the password of a user in the database while the user is logged in

    Arguments:
        email   (string) - The user's email\n
        oldpass (string) - The user's old password\n
        pass1   (string) - The user's new password\n
        pass2   (string) - The user's password entered again to check that the password was entered correctly

    Exceptions:
        InputError - If the token is invalid, if the password is incorrect or if the user can't be found

    Return Value:
        N/A
    '''
    user = User.query.filter_by(email=email).first()
    numbers = sum(c.isdigit() for c in pass1)
    letters = sum(c.isalpha() for c in pass1)
    if user:
        if hash_password(oldpass) != user.password:
            flash('Password entered is incorrect', category='error')
            raise InputError(description='Password entered is incorrect')
        check_pass(numbers, letters, pass1, pass2)
        flash('Password has been changed', category='success')
        change_password(email, pass1)
    else:
        flash('Cannot find profile', category='error')
        raise InputError(description='Cannot find profile')


def edit_details(id, first_name, last_name, profile_image):
    '''
    Changes the personal information of a user in the database

    Arguments:
        id              (int) - The user's email\n
        firstName       (string) - The user's first name\n
        lastName        (string) - The user's last name\n
        profile_image   (string) - The location of the user's profile picture stored in the backend

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(id=id).first()
    if user:
        user.firstName = first_name
        user.lastName = last_name
        user.profile_image = profile_image
        db.session.commit()
        flash('Profile details have been edited !', category='success')


def change_password(email, password):
    '''
    Reverts the custom profile picture of a uesr to the default picture while the user is logged in

    Arguments:
        id  (int) - The user's id

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    user.password = hash_password(password)
    db.session.commit()
    return True


def change_picture(id, url):
    '''
    Reverts the custom profile picture of a uesr to the default picture while the user is logged in

    Arguments:
        id  (int) - The user's id

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(id=id).first()
    if user is None:
        return False
    user.profilePic = url
    db.session.commit()
    return True
