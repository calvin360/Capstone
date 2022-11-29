'''
Database for the backend of the website.
Made by Ajay Arudselvam, Calvin Lau and Keerthivasan Gopalraj, Shaun Zheng
'''

from datetime import datetime

from . import db
from Backend.auth_helper import *
from flask import flash
import os
import fnmatch

following_channel = db.Table('following_channel',
                             db.Column('user_email', db.Integer,
                                       db.ForeignKey('user.email')),
                             db.Column('following_email', db.Integer,))

like_channel = db.Table('like_channel',
                        db.Column('user_email', db.Integer,
                                  db.ForeignKey('user.email')),
                        db.Column('recipes_id', db.Integer,
                                  db.ForeignKey('recipe.recipe_id'))
                        )

dislike_channel = db.Table('dislike_channel',
                           db.Column('user_email', db.Integer,
                                     db.ForeignKey('user.email')),
                           db.Column('recipes_id', db.Integer,
                                     db.ForeignKey('recipe.recipe_id'))
                           )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String(200), unique=True)
    picture = db.Column(db.String(1000))
    reset_code = db.Column(db.String(6))
    username = db.Column(db.Integer, unique=True)
    following = db.relationship('User', secondary=following_channel,
                                primaryjoin=email == following_channel.c.user_email,
                                secondaryjoin=email == following_channel.c.following_email,
                                backref='followers')
    like = db.relationship(
        'Recipe', secondary=like_channel, backref='liked_users')
    dislike = db.relationship(
        'Recipe', secondary=dislike_channel, backref='disliked_users')
    number_followers = db.Column(db.Integer, default=0)
    number_following = db.Column(db.Integer, default=0)
    number_recipe_uploaded = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.String(100))
    saved_recipes = db.Column(db.Text)
    favourite = db.Column(db.Integer, default=-1)


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(200))
    email = db.Column(db.String(100))
    #recipePicture = db.Column(db.String(2000))
    recipe_ingredients = db.Column(db.Text)
    recipe_method = db.Column(db.Text)
    recipe_description = db.Column(db.Text)
    recipe_created_time = db.Column(db.DateTime, default=datetime.now())
    recipeLikes = db.Column(db.Integer, default=0)
    recipeDislikes = db.Column(db.Integer, default=0)
    prep_time = db.Column(db.Integer, default=0)
    cook_time = db.Column(db.Integer, default=0)
    servings = db.Column(db.Integer, default=0)
    recipe_image = db.Column(db.String(100))
    recipe_video = db.Column(db.String(100))
    meal_type = db.Column(db.String(20))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    recipe_id = db.Column(db.Integer)
    comment = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now())
    username = db.Column(db.Integer)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    comment = db.Column(db.Text)
    subject = db.Column(db.String(100))
    time = db.Column(db.DateTime, default=datetime.now())


def add_user(first_name, last_name, password, email, username):
    '''
    Adds a user to the database

    Arguments:
        first_name (string) - First name of the user\n
        last_name  (string) - Last name of the user\n
        password   (string) - Password of the user\n
        email      (string) - email of the user\n
        username   (string) - username of the user

    Exceptions:
        N/A

    Return Value:
        Returns a dictionary of the user's details
    '''
    user = User(email=email, firstName=first_name, lastName=last_name,
                password=password, username=username, profile_image='default',
                saved_recipes=',')
    db.session.add(user)
    db.session.commit()
    return {"firstName": user.firstName, "lastName": user.lastName,
            "email": user.email, "id": user.id, "username": user.username}


def remove_user(email):
    '''
    Removes a user from the database

    Arguments:
        email (string) - email of the user

    Exceptions:
        N/A

    Return Value:
        Returns true if successful and false otherwise
    '''
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    else:
        recipes = Recipe.query.filter_by(email=email).all()
        comments = Comment.query.filter_by(email=email).all()
        for recipe in recipes:
            db.session.delete(recipe)
        for comment in comments:
            db.session.delete(comment)
        followed = user.following
        for u in followed:
            u.number_followers = u.number_followers - 1
        following = user.followers
        for u in following:
            u.number_following = user.number_following - 1
        db.session.delete(user)
        db.session.commit()
        return True


def add_recipe(recipe_name, email, recipe_ingredients, recipe_method, recipe_description,
               prep_time, cook_time, servings, recipe_image, recipe_video, meal_type):
    '''
    Adds a recipe to the database

    Arguments:
        recipe_name        (string) - The recipe name\n
        email              (string) - The email of the user trying to edit the recipe\n
        recipe_ingredients (string) - The ingredients in the recipe\n
        recipe_method      (string) - The instructions for the recipe\n
        recipe_description (string) - A brief description of the recipe\n
        prep_time          (int)    - The required time to prepare the ingredients for the recipe\n
        cook_time          (int)    - The required cooking time to finish cooking the meal\n
        servings           (int)    - The amount of people that can be fed using the recipe\n
        recipe_image       (string) - The location of where the recipe image is being stored\n
        recipe_video       (string) - The link to the instructional video for the recipe\n
        meal_type          (string) - The type of meal the recipe is trying to achieve\n

    Exceptions:
        N/A

    Return Value:
        Returns a dictionary with all the fields of the Recipe database
    '''
    recipe = Recipe(recipe_name=recipe_name, email=email,
                    recipe_ingredients=recipe_ingredients, recipe_method=recipe_method,
                    recipe_description=recipe_description, prep_time=prep_time, cook_time=cook_time,
                    servings=servings, recipe_image=recipe_image, recipe_video=recipe_video, meal_type=meal_type)
    db.session.add(recipe)
    user = User.query.filter_by(email=email).first()
    user.number_recipe_uploaded = user.number_recipe_uploaded + 1
    db.session.commit()
    return {"recipe_id": recipe.recipe_id, "recipe_name": recipe.recipe_name, "email": recipe.email,
            "recipe_method": recipe.recipe_method, "recipe_ingredients": recipe.recipe_ingredients,
            "recipe_description": recipe.recipe_description, "recipeLikes": recipe.recipeLikes,
            "recipeDislikes": recipe.recipeDislikes, "recipe_created_time": recipe.recipe_created_time,
            "recipe_image": recipe.recipe_image}


def remove_recipe(id, email):
    '''
    Removes a recipe from the database

    Arguments:
        id    (int)    - id of the recipe\n
        email (string) - email of the user

    Exceptions:
        N/A

    Return Value:
        Returns true if successful and false otherwise
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return False
    elif recipe.email == email:
        db.session.delete(recipe)
        user = User.query.filter_by(email=email).first()
        user.number_recipe_uploaded = user.number_recipe_uploaded - 1
        db.session.commit()
        flash('Recipe has been removed', category='success')
        return True
    else:
        flash('User is not allowed to remove this recipe', category='error')
        raise InputError(description='Entered email is invalid')


def remove_profile_pic(id):
    '''
    Removes the profile picture of a user

    Arguments:
        id    (int)    - id of the user

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    user = User.query.filter_by(id=id).first()
    if user:
        user.profile_image = 'default'
        db.session.commit()
        flash('Profile picture is retore to default!', category='success')


def add_comment(email, recipe_id, comment):
    '''
    Adds a comment on a recipe

    Arguments:
        email     (string) - email of the user\n
        recipe_id (int)    - id of the recipe\n
        comment   (string) - the comment to be added

    Exceptions:
        N/A

    Return Value:
        Returns basic information on the comment
    '''
    user = User.query.filter_by(email=email).first()
    comment = Comment(email=email, recipe_id=recipe_id,
                      comment=comment, username=user.username)
    db.session.add(comment)
    db.session.commit()
    return {"email": comment.email, "recipe_id": comment.recipe_id, "comment": comment.comment}


def add_feedback(email, subject, comment):
    '''
    Adds a feedback about the website

    Arguments:
        email     (string) - email of the user\n
        subject   (int)    - subject of the feedback\n
        comment   (string) - the feedback

    Exceptions:
        N/A

    Return Value:
        Returns basic information on the feedback
    '''
    feedback = Feedback(email=email, subject=subject, comment=comment)
    db.session.add(feedback)
    db.session.commit()
    return {"email": feedback.email, "subject": feedback.subject, "comment": feedback.comment}

def remove_image(path, pattern):
    '''
    Adds a feedback about the website

    Arguments:
        path     (string) - image path 
        pattern   (string) - image pattern

    Exceptions:
        N/A

    Return Value:
        nothing
    '''

    found = False
    for _, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                os.remove(path + '/' + name)
                found = True
                break
        if found:
            break

    return