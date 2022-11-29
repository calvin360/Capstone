'''
Functions for searching for users in the database.
Made by Ajay Arudselvam
'''

from difflib import SequenceMatcher
from Database.Data import *
from Backend.auth_helper import *
from Backend.helper import *


def search_users(text):
    '''
    Returns a list of users which fufill the search criteria

    Arguments:
        text (String) - The keywords that we are looking for

    Exceptions:
        N/A

    Return Value:
        Returns a list with the related users
    '''
    users = User.query.all()
    l = []

    for user in users:
        score = 0
        score = score + SequenceMatcher(None, user.username, text).ratio()
        if text in user.username:
            score = score + 1
        score = score + SequenceMatcher(None, user.email, text).ratio()
        if text in user.email:
            score = score + 1
        l.append((user.id, score))
    reps = []

    results = len(users)//3
    for x in range(results):
        sort = sorted(l, key=lambda x: x[1], reverse=True)[x]
        id = sort[0]
        similarlity = sort[1]
        if similarlity > 0.6:
            searched_user = User.query.filter_by(id=id).first()
            reps.append(searched_user)

    return reps

def recommendation(recipe):
    '''
    Returns a list of recipes which closely match the given recipe

    Arguments:
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns a list with the recommended recipes
    '''
    recipes = Recipe.query.all()
    l = []

    for r in recipes:
        if r.recipe_id != recipe.recipe_id:
            score = 0
            score = score + \
                SequenceMatcher(None, r.recipe_ingredients,
                                recipe.recipe_ingredients).ratio()
            score = score + \
                SequenceMatcher(None, r.recipe_name,
                                recipe.recipe_name).ratio()
            l.append((r.recipe_id, score))

    reps = []
    amount = min(3, len(recipes))
    for x in range(amount):
        id = sorted(l, key=lambda x: x[1], reverse=True)[x][0]
        recommended_recipe = Recipe.query.filter_by(recipe_id=id).first()
        reps.append(recommended_recipe)
    return reps


def search_recipe(text):
    '''
    Returns a list of recipes which fufill the search criteria

    Arguments:
        text (String) - The keywords that we are looking for

    Exceptions:
        N/A

    Return Value:
        Returns a list with the related recipes
    '''
    recipes = Recipe.query.all()
    l = []

    for r in recipes:
        score = 0
        user = User.query.filter_by(email=r.email).first()
        score = score + \
            SequenceMatcher(None, r.recipe_ingredients, text).ratio()
        if text in r.recipe_ingredients:
            score = score + 0.5
        score = score + SequenceMatcher(None, r.recipe_name, text).ratio()
        if text in r.recipe_name:
            score = score + 1.5
        score = score + SequenceMatcher(None, r.recipe_method, text).ratio()
        if text in r.recipe_method:
            score = score + 0.5
        score = score + \
            SequenceMatcher(None, r.recipe_description, text).ratio()
        if text in r.recipe_description:
            score = score + 1.5
        score = score + SequenceMatcher(None, r.email, text).ratio()
        if text in r.email:
            score = score + 1
        score = score + SequenceMatcher(None, user.username, text).ratio()
        if text in user.username:
            score = score + 1
        score = score + SequenceMatcher(None, r.meal_type, text).ratio()
        if r.meal_type in text:
            score = score + 0.5
        l.append((r.recipe_id, score))
    reps = []
    results = len(recipes)//3
    for x in range(results):
        sort = sorted(l, key=lambda x: x[1], reverse=True)[x]
        id = sort[0]
        similarlity = sort[1]
        if similarlity > 1:
            recommended_recipe = Recipe.query.filter_by(recipe_id=id).first()
            reps.append(recommended_recipe)
    return reps

