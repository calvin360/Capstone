'''
Functions for managing following users.
Made by Ajay Arudselvam
'''

from flask import flash
from Database.Data import *
from Backend.auth_helper import *
from Backend.helper import *
from Backend.error import InputError


def get_following(user):
    '''
    Returns a list of users that the user is following

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a list of users
    '''
    return user.following


def get_followers(user):
    '''
    Returns a list of users that are following the user

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a list of users
    '''
    return user.followers


def add_following(user, following_user):
    '''
    Adds a new user to the following list

    Arguments:
        user (User) - The database representing a user
        following_user (User) - The user that user wants to follow

    Exceptions:
        N/A

    Return Value:
        Returns a list of users
    '''
    followed = get_following(user)
    if following_user in followed:
        flash('You already follow this user ', category='error')
        raise InputError(description='You are already following this user')
    else:
        user.following.append(following_user)
        user.number_following += 1
        following_user.number_followers += 1
        db.session.commit()
        flash('Successfully following user', category='success')


def remove_following(user, following_user):
    '''
    Removes a user from the following list

    Arguments:
        user (User) - The database representing a user
        following_user (User) - The user that user wants to unfollow

    Exceptions:
        InputError - If the following_user isn't in the following list

    Return Value:
        N/A
    '''
    followed = get_following(user)
    if following_user in followed:
        user.following.remove(following_user)
        user.number_following -= 1
        following_user.number_followers -= 1
        db.session.commit()
        flash('You no longer follow this user', category='success')
    else:
        flash('You do not follow this user ', category='error')
        raise InputError(description='You do not follow this user')



def is_following(user, following_user):
    '''
    Checks if a user is in another user's following list

    Arguments:
        user (User) - The database representing a user
        following_user (User) - The user that is being checked

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    return following_user in get_following(user)


def following_recipes(user):
    '''
    Gets a list of recipes a user is following

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a list of recipes
    '''
    # emails = []
    recipes = Recipe.query.all()
    # for u in followed:
    #     emails.append(u.email)
    emails = [u.email for u in get_following(user)]
    recipes = Recipe.query.filter(Recipe.email.in_(
        emails)).order_by(Recipe.recipe_id.desc()).all()
    return recipes
