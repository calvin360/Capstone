'''
General helper functions for using the database.
Made by Ajay Arudselvam, Calvin Lau and Keerthivasan Gopalraj
'''
import os
import fnmatch

from flask import flash
from Database.Data import *
from Backend.auth_helper import *
from Backend.error import InputError


def exists_email(email):
    '''
    checks if an email exists in the database

    Arguments:
        email (string) - The email that we are looking for

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(email=email).first()
    return user is not None


def exists_recipe(recipe_id):
    '''
    checks if a recipe exists in the database

    Arguments:
        recipe (string) - The recipe that we are looking for

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    return recipe is not None


def username_exists(username):
    '''
    checks if a username exists in the database

    Arguments:
        username (string) - The uesrname that we are looking for

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(username=username).first()
    return user is not None


def exists_token(id):
    '''
    checks if a token exists in the database

    Arguments:
        token (string) - The token that we are looking for

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(id=id).first()
    return user.token is not None


def add_token(user, token):
    '''
    Adds a token to the specified user

    Arguments:
        user  (User)   - The database representing a user\n
        token (string) - The token representing an active user session

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user.token = token
    db.session.commit()


def get_user_id(id):
    '''
    Gets the user by id

    Arguments:
        id (int) - An id representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a dictionary of user details, otherwise returns false
    '''
    user = User.query.filter_by(id=id).first()
    if user is None:
        return False
    else:
        return {"firstName": user.firstName, "lastName": user.lastName,
                "email": user.email, "id": user.id, "picture": user.picture}


def get_user_email(email):
    '''
    Gets the user by email

    Arguments:
        email (int)   - The email of a user

    Exceptions:
        N/A

    Return Value:
        Returns a dictionary of user details, otherwise returns false
    '''
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    else:
        return {"firstName": user.firstName, "lastName": user.lastName,
                "email": user.email, "id": user.id, "picture": user.picture}


def add_reset_code(id, code):
    '''
    Adds a reset code to the user database

    Arguments:
        id   (int)    - An id representing a user\n
        code (string) - A randomly generated code

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(id=id).first()
    if user is None:
        return
    user.reset_code = code
    db.session.commit()


# def remove_reset_code(Id):
#     user = User.query.filter_by(id=Id).first()
#     if user == None:
#         return False
#     user.resetCode = None
#     db.session.commit()
#     return True


def get_recipe(id):
    '''
    Gets a recipe from the database by id

    Arguments:
        id (int) - An id representing a recipe

    Exceptions:
        InputError - If the id doesn't correspond to an existing recipe

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        flash('recipe does not exist', category='error')
        raise InputError(description='bad id')
    return {"recipe_id": recipe.recipe_id, "recipe_name": recipe.recipe_name,
            "email": recipe.email, "recipe_method": recipe.recipe_method,
            "recipe_ingredients": recipe.recipe_ingredients}


def get_profile_pic(username):
    '''
    Gets the profile picture of a user

    Arguments:
        username (string) - The username of a user

    Exceptions:
        N/A

    Return Value:
        Returns the location of the profile picture
    '''
    path = 'Database/static/images/userProfileImages'
    pattern = username + '.*'
    found = False
    profile_pic = ''
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                profile_pic = os.path.join(root, name)
                profile_pic = profile_pic.replace('Database', '..')
                found = True
                break  
    if not found:
        profile_pic = '../static/images/userProfileImages/default.jpg'
        
    return profile_pic
