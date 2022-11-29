'''
Functions for modifing and checking recipes.
Made by Ajay Arudselvam, Calvin Lau and Keerthivasan Gopalraj
'''


from flask import flash

from Database.Data import *
from Backend.error import InputError, AccessError
from Backend.auth_helper import *
from Backend.helper import *


def check_recipe(recipe_name, email):
    '''
    Checks if the recipe name and email follow the required format

    Arguments:
        email       (string) - The user's email address\n
        recipe_name (string) - The name of the recipe

    Exceptions:
        InputError - If the provided email isn't in the database,\n
                     or if the recipe name is too long

    Return Value:
        Returns a dictionary with the user id and user token
    '''
    if not exists_email(email):
        flash('Email does not exist', category='error')
        raise InputError(description='Invalid email')
    if len(recipe_name) > 200:
        flash('Recipe name is too long', category='error')
        raise InputError(description='Invalid name length')
    return True


def get_liked_recipes(user):
    '''
    Gets a list of the user's liked recipes

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a database with the recipe ids that the user likes
    '''
    return user.like


def get_liked_users(recipe):
    '''
    Gets a list of the users who like a recipe

    Arguments:
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns a database with the user emails that like the recipe
    '''
    return recipe.liked_users


def add_like(user, recipe):
    '''
    Adds a liked recipe to the user's liked list and increments the
    amount of likes on a recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    if not recipe in get_liked_recipes(user):
        user.like.append(recipe)
        db.session.commit()
        like_recipe(recipe.recipe_id)


def get_disliked_recipes(user):
    '''
    Gets a list of recipes that a user dislikes

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a database with the user emails that dislike the recipe
    '''
    return user.dislike


def get_disliked_users(recipe):
    '''
    Gets a list of the users who dislike a recipe

    Arguments:
        user (User) - The database representing a user

    Exceptions:
        N/A

    Return Value:
        Returns a database with the user emails that dislike the recipe
    '''
    return recipe.disliked_users


def add_dislike(user, recipe):
    '''
    Adds a disliked recipe to the user's disliked list and increments the
    amount of dislikes on a recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    if not recipe in get_disliked_recipes(user):
        user.dislike.append(recipe)
        db.session.commit()
        dislike_recipe(recipe.recipe_id)


def is_liked(user, recipe):
    '''
    Checks if a user has already liked a recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns true if recipe has been liked and false otherwise
    '''
    return recipe in get_liked_recipes(user)


def is_disliked(user, recipe):
    '''
    Checks if a user has already dsliked a recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns true if recipe has been disliked and false otherwise
    '''
    return recipe in get_disliked_recipes(user)


def remove_like(user, recipe):
    '''
    Removes a liked recipe from a user's liked list and decrements the likes
    on the recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    if recipe in get_liked_recipes(user):
        user.like.remove(recipe)
        db.session.commit()
        remove_like_recipe(recipe.recipe_id)


def remove_dislike(user, recipe):
    '''
    Removes a disliked recipe from a user's disliked list and decrements the dislikes
    on the recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    if recipe in get_disliked_recipes(user):
        user.dislike.remove(recipe)
        db.session.commit()
        remove_dislike_recipe(recipe.recipe_id)


def order_by_time():
    '''
    Returns a list of recipes in ascending order based on when they were created

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        Returns a list with the ordered recipes
    '''
    return Recipe.query.order_by(Recipe.recipe_id.desc()).all()


def order_by_likes():
    '''
    Returns a list of recipes in ascending order based the amount of likes

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        Returns a list with the ordered recipes
    '''
    return Recipe.query.order_by(Recipe.recipeLikes.desc()).all()


def order_by_dislikes():
    '''
    Returns a list of recipes in ascending order based the amount of dislikes

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        Returns a list with the ordered recipes
    '''
    return Recipe.query.order_by(Recipe.recipeDislikes).all()



def select_favourite(email, recipe_id):
    '''
    Sets the favourite recipe for a given contributor

    Arguments:
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns true if successful and false otherwise
    '''
    user = User.query.filter_by(email=email).first()
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if recipe.email == email:
        user.favourite = recipe_id
        db.session.commit()
        flash('Favourite recipe chosen !', category='success')
        return True
    else:
        flash('You are not the contributor of this recipe !', category='success')
        return False


def remove_favourite(email, recipeId):
    '''
    Removes the favourite recipe for a given contributor

    Arguments:
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns true if successful and false otherwise
    '''
    user = User.query.filter_by(email=email).first()
    recipe = Recipe.query.filter_by(recipe_id=recipeId).first()
    if recipe.email == email:
        user.favourite = -1
        db.session.commit()
        flash('Favourite recipe been removed !', category='success')
        return True
    else:
        flash('You are not the contributor of this recipe !', category='success')
        return False


def is_favourite(user, recipe):
    '''
    Checks if a recipe is the user's favourite recipe

    Arguments:
        user   (User)   - The database representing a user\n
        recipe (Recipe) - The database representing a recipe

    Exceptions:
        N/A

    Return Value:
        Returns true if the given recipe is the user's favourite and false otherwise
    '''
    return user.favourite == recipe.recipe_id


def edit_recipe_1(id, email, recipe_name, recipe_ingredients, recipe_method, recipe_description, picture,
                  prep_time, cook_time, servings, recipe_image, recipe_video, meal_type):
    '''
    Updates an existing recipe with new information

    Arguments:
        id                 (int)    - The recipe id\n
        email              (string) - The email of the user trying to edit the recipe\n
        recipe_name        (string) - The recipe name\n
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
        AccessError - If the user trying the edit the recipe isn't the orignal uploader

    Return Value:
        Returns a dictionary with all the fields of the Recipe database
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return False
    elif recipe.email == email:
        recipe.recipe_name = recipe_name
        recipe.recipe_ingredients = recipe_ingredients
        recipe.recipe_method = recipe_method
        recipe.recipe_description = recipe_description
        recipe.created_time = datetime.now()
        recipe.prep_time = prep_time
        recipe.cook_time = cook_time
        recipe.servings = servings
        recipe.recipe_image = recipe_image
        recipe.recipe_video = recipe_video
        recipe.meal_type = meal_type

        db.session.commit()
        flash('Recipe has been updated', category='success')
        return {"recipe_id": recipe.recipe_id, "recipe_name": recipe.recipe_name,
                "email": recipe.email, "recipe_method": recipe.recipe_method,
                "recipe_ingredients": recipe.recipe_ingredients, "recipe_description": recipe.recipe_description,
                "recipeLikes": recipe.recipeLikes, "recipeDislikes": recipe.recipeDislikes,
                "recipe_created_time": recipe.recipe_created_time}
    else:
        flash('User is not allowed to edit this recipe', category='error')
        raise AccessError(description='Entered email is invalid')


def like_recipe(recipe_id):
    '''
    Increments the amount of likes on a recipe

    Arguments:
        recipe_id (int) - The id of the recipe in the database

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe.recipeLikes += 1
    db.session.commit()


def remove_like_recipe(recipe_id):
    '''
    Decrements the amount of likes on a recipe

    Arguments:
        recipe_id (int) - The id of the recipe in the database

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe.recipeLikes -= 1
    db.session.commit()
    return True


def dislike_recipe(recipe_id):
    '''
    Increments the amount of dislikes on a recipe

    Arguments:
        recipe_id (int) - The id of the recipe in the database

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe.recipeDislikes += 1
    db.session.commit()
    return True


def remove_dislike_recipe(recipe_id):
    '''
    Decrements the amount of dislikes on a recipe

    Arguments:
        recipe_id (int) - The id of the recipe in the database

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    recipe.recipeDislikes -= 1
    db.session.commit()
    return True


def save_recipe(id, email):
    '''
    Saves a recipe to the saved list in the user's database

    Arguments:
        id    (int)    - The id of the recipe in the database\n
        email (string) - The email of the user trying to save the recipe

    Exceptions:
        InputError - If the recipe has already been saved

    Return Value:
        Returns false if the recipe or user doesn't exist
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return False
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False

    saved = user.saved_recipes.split(",")
    if str(id) in saved:
        flash('Recipe has already been saved', category='error')
        raise InputError(description='Recipe already in list')

    user.saved_recipes += str(id)+','
    db.session.commit()
    flash('Recipe has been saved!', category='success')


def unsave_recipe(id, email):
    '''
    Removes a recipe from the saved list in the user's database

    Arguments:
        id    (int)    - The id of the recipe in the database\n
        email (string) - The email of the user trying to save the recipe

    Exceptions:
        InputError - If the recipe is not in the list
    Return Value:
        Returns false if the recipe or user doesn't exist
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return False
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False

    saved = user.saved_recipes.split(",")
    if str(id) not in saved:
        flash('Recipe has not been saved', category='error')
        raise InputError(description='Recipe not in list')
    saved.remove(str(id))
    user.saved_recipes = ','.join(saved)
    db.session.commit()
    flash('Recipe has been removed!', category='success')


def get_saved_recipes(email):
    '''
    Gets the saved recipes for a user

    Arguments:
        email (string) - The email of the user trying to save the recipe

    Exceptions:
        N/A

    Return Value:
        Returns false if the user doesn't exist or a list with the user's saved recipes
    '''
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False

    saved = user.saved_recipes.split(",")
    ids = []
    recipes = Recipe.query.all()
    # for u in saved:
    #     ids.append(u)
    ids = [x for x in saved]
    recipes = Recipe.query.filter(Recipe.recipe_id.in_(ids)).all()
    return recipes


def is_saved(id, email):
    '''
    Checks if a recipe is in a user's saved list

    Arguments:
        id    (int)    - The id of the recipe in the database\n
        email (string) - The email of the user trying to save the recipe

    Exceptions:
        InputError - If the recipe has already been saved

    Return Value:
        Returns false if the recipe or user doesn't exist
    '''
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return False
    return recipe in get_saved_recipes(email)


def get_ingredients(id):
    '''
    Gets the ingredients of a recipe

    Arguments:
        id (int) - The id of the recipe in the database

    Exceptions:
        N/A

    Return Value:
        Returns a list of ingredients
    '''
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    if recipe is None:
        return

    ingredients = recipe.recipe_ingredients.split("\r\n")
    tmp = [i for i in ingredients if i != '']
    out = []
    for i in tmp:
        res = i.split(',')
        out.append(res[0])
    return out
