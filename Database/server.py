'''
Server file with the routes for frontend and backend features.
Made by Ajay Arudselvam, Calvin Lau and Keerthivasan Gopalraj, Shaun Zheng,
Chowdhury Rubaiat Bin Mowla
'''
import os
import fnmatch
import time

from Backend.recipe import *
from .Data import *
from Backend.auth import *
from Backend.following import *
from Backend.helper import *
from Backend.search import *
from flask import Blueprint, request, flash, redirect, url_for, render_template, session, redirect, url_for, g


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


@apps.route("/logged")
def logged():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipes = Recipe.query.all()
    return render_template('logged.html', recipes=recipes)


@apps.route("/logged_like")
def logged_like():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipes = order_by_likes()
    return render_template('logged.html', recipes=recipes)


@apps.route("/logged_dislike")
def logged_dislike():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipes = order_by_dislikes()
    return render_template('logged.html', recipes=recipes)


@apps.route("/logged_time")
def logged_time():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipes = order_by_time()
    return render_template('logged.html', recipes=recipes)


@apps.route("/register", methods=["GET", "POST"])
def appRegister():
    if request.method == "POST":
        session.pop('email', None)
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        try:
            register(firstname, lastname, password1,
                     email, username, password2)
            session['email'] = email
            return redirect(url_for('apps.logged'))
        except:
            return render_template("failRegister.html", firstname=firstname, lastname=lastname, username=username, email=email, password1=password1, password2=password2)
    else:
        return render_template("register.html")


@apps.route("/login", methods=["GET", "POST"])
def appLogin():
    if request.method == "POST":
        session.pop('email', None)
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            login(email, password)
            session['email'] = email
            return redirect(url_for('apps.logged'))
        except:
            return render_template("login.html")
    else:
        return render_template("login.html")


@apps.route("/forgotPass/<email>", methods=["GET", "POST"])
def forgotPass(email):

    if request.method == "POST":
        code = request.form.get("text")
        password = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        try:
            reset_password(email, user.token, code, password, password2)
            return redirect(url_for('apps.appLogin'))
        except:
            return render_template("failForgotPass.html", code=code, password=password, password2=password2, email=email)
    else:
        return render_template("forgotPass.html", email=email)


@apps.route("/resetPass", methods=["GET", "POST"])
def resetPass():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        email = session['email']
        password1 = request.form.get('password2')
        password2 = request.form.get('password3')
        oldpass = request.form.get("password1")
        try:
            change_password_request(email, oldpass, password1, password2)
            return redirect(url_for('apps.logged'))
        except:
            return render_template("resetPass.html")
    else:
        return render_template("resetPass.html")


@apps.route("/requestPassword", methods=["GET", "POST"])
def requestPassword():
    if request.method == "POST":
        email = request.form.get("email")
        try:
            request_password_reset(email)
            return redirect(url_for('apps.forgotPass', email=email))
        except:
            return render_template("requestPassword.html")
    else:
        return render_template("requestPassword.html")


@apps.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    profilePic = '/static/images/userProfileImages/' + g.user.profile_image + '.jpg'

    return render_template('profile.html', pic=profilePic)


@apps. route('/logout')
def appLogout():
    if "email" in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        logout(user.token)
    session.pop("email", None)
    return redirect(url_for('apps.appLogin'))


@apps.route("/add/recipe", methods=["GET", "POST"])
def addRecipe():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        email = session['email']
        recipe_name = request.form.get("recipe_name")
        recipe_ingredients = request.form.get("recipe_ingredients")
        recipe_method = request.form.get("recipe_method")
        recipe_description = request.form.get("recipe_description")
        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")
        meal_type = request.form.get("meal_type")
        recipe_image = str(time.time())

        # Photo Upload
        file1 = request.files['file']
        UPLOAD_FOLDER = 'Database/static/images/recipeImages'
        filename = file1.filename
        filename = recipe_image + '.jpg'
        file1.save(os.path.join(UPLOAD_FOLDER, filename))

        # Video Upload
        recipe_video = ''

        video_file = request.form.get("input_video")
        video_file = video_file.replace("watch?v=", "embed/")
        if video_file != '':
            recipe_video = video_file
        else:
            recipe_video = ''

        add_recipe(recipe_name, email,
                   recipe_ingredients, recipe_method, recipe_description, prep_time, cook_time, servings, recipe_image, recipe_video, meal_type)['recipe_id']
        return redirect(url_for('apps.logged'))
    else:
        return render_template("addRecipe.html")


@apps.route("/remove/recipe", methods=["POST"])
def delete_recipe():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        id = request.args.get('id', 0)
        email = session['email']

        recipe = Recipe.query.filter_by(recipe_id=id).first()
        path = 'Database/static/images/recipeImages'
        pattern = recipe.recipe_image + '.*'
        remove_image(path, pattern)
        remove_recipe(id, email)
        return redirect(url_for('apps.myRecipe'))
    else:
        return render_template("addReceipt.html")




@apps.route('/profile/deleteProfile', methods=["GET"])
def deleteProfilePage():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "GET":
        return render_template("deleteAccount.html")


@apps.route('/profile/deleteProfile/confirm', methods=["GET", "POST"])
def deleteProfile():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        password = request.form.get('password')
        if "email" in session:
            email = session['email']
            user = User.query.filter_by(email=email).first()
            try:
                deleteAccount(user.token, password)
                path = 'Database/static/images/userProfileImages'
                pattern = g.user.profile_image + '.*'
                if g.user.profile_image != 'default':
                    remove_image(path, pattern)
                return redirect(url_for('apps.appLogin'))
            except:
                return redirect(url_for('apps.deleteProfilePage'))
    if request.method == "GET":
        return redirect(url_for('apps.deleteProfilePage'))


@apps.route('/profile/changeProfile', methods=["GET"])
def changeProfile():
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    profilePic = '/static/images/userProfileImages/' + g.user.profile_image + '.jpg'
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    return render_template('changeProfile.html', pic=profilePic)


@apps.route('/profile/changeProfile/save', methods=['POST'])
def saveProfileChange():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        file1 = request.files['file']

        profile_image = ''
        if file1.filename != '':
            profile_image = str(time.time())
            UPLOAD_FOLDER = 'Database/static/images/userProfileImages'
            filename = file1.filename

            filename = profile_image + '.jpg'
            file1.save(os.path.join(UPLOAD_FOLDER, filename))

            path = 'Database/static/images/userProfileImages'
            pattern = g.user.profile_image + '.*'
            if g.user.profile_image != 'default':
                remove_image(path, pattern)
        else:
            profile_image = g.user.profile_image
        edit_details(g.user.id, firstName, lastName, profile_image)

        return redirect(url_for('apps.profile'))
    return redirect(url_for('apps.profile'))


@apps.route('/profile/removeProfilePic', methods=['POST'])
def removeProfilePic():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == "POST":
        path = 'Database/static/images/userProfileImages'
        pattern = g.user.profile_image + '.*'
        if g.user.profile_image != 'default':
            remove_image(path, pattern)
            remove_profile_pic(g.user.id)
    return redirect(url_for('apps.profile'))


@apps.route("/profile/myRecipe", methods=['GET'])
def myRecipe():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipes = Recipe.query.filter_by(email=g.user.email).all()
    if len(recipes) == 0:
        return render_template('noRecipe.html')
    return render_template('myRecipe.html', recipes=recipes, num=len(recipes))


@apps.route('/myRecipe/detail', methods=['GET'])
def my_recipe_detail():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipe_id = request.args.get('id', 0)
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    comments = Comment.query.all()
    current_user = User.query.filter_by(email=session['email']).first()
    if recipe.recipe_video == '':
        display1 = 'display'
    else:
        display1 = ''
    if is_favourite(current_user, recipe):
        favourite = "Favourite"
    else:
        favourite = "Select as Favourite"
    pic = '../static/images/userProfileImages/' + current_user.profile_image + '.jpg'
    return render_template('myRecipeDetail.html', recipe=recipe, comments=comments, pic=pic, favourite=favourite, display1=display1, user=current_user)


@apps.route("/profile/myRecipe/edit/<id>", methods=['GET'])
def edit_recipe(id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    recipe = Recipe.query.filter_by(recipe_id=id).all()
    return render_template('editRecipe.html', recipe=recipe[0])


@apps.route("/othersprofile/<email_r>", methods=['GET'])
def view_profile(email_r):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    other_user = User.query.filter_by(email=email_r).first()
    current_user = User.query.filter_by(email=session['email']).first()
    pic = '../static/images/userProfileImages/' + other_user.profile_image + '.jpg'
    sub = ""

    if is_following(current_user, other_user):
        sub = 'unsubscribe'
    else:
        sub = 'subscribe'

    if email_r == g.user.email:
        return redirect(url_for('apps.profile'))

    return render_template('othersProfile.html', user=other_user, pic=pic, sub=sub)


@apps.route("/othersrecipe/<email_r>", methods=['GET'])
def view_recipe(email_r):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    user = User.query.filter_by(email=email_r).first()
    recipes = Recipe.query.filter_by(email=user.email).all()

    return render_template('otherRecipe.html', recipes=recipes, num=len(recipes), user=user)


@apps.route("/profile/myRecipe/edit/save", methods=['POST'])
def save_edit_recipe():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    email = session['email']
    id = int(request.args.get('id', 0))
    recipe_name = request.form.get("recipe_name")
    recipe_ingredients = request.form.get("recipe_ingredients")
    recipe_method = request.form.get("recipe_method")
    recipe_description = request.form.get("recipe_description")
    picture = request.form.get("picture")
    prep_time = request.form.get("prep_time")
    cook_time = request.form.get("cook_time")
    servings = request.form.get("servings")
    file1 = request.files['file']
    meal_type = request.form.get("meal_type")
    recipe_image = ''
    if check_recipe(recipe_name, email):

        # Photo
        if file1.filename != '':
            recipe_image = str(time.time())
            UPLOAD_FOLDER = 'Database/static/images/recipeImages'
            recipe = Recipe.query.all()
            filename = file1.filename
            filename = recipe_image + '.jpg'
            file1.save(os.path.join(UPLOAD_FOLDER, filename))

            recipe = Recipe.query.filter_by(recipe_id=id).first()
            path = 'Database/static/images/recipeImages'
            pattern = recipe.recipe_image + '.*'
            remove_image(path, pattern)
        else:
            recipe = Recipe.query.filter_by(recipe_id=id).first()
            recipe_image = recipe.recipe_image

        # Video
        recipe_video = ''

        video_file = request.form.get("input_video")
        video_file = video_file.replace("watch?v=", "embed/")
        if video_file != '':
            recipe_video = video_file
        else:
            recipe = Recipe.query.filter_by(recipe_id=id).first()
            recipe_video = recipe.recipe_video

        edit_recipe_1(id, email, recipe_name, recipe_ingredients,
                      recipe_method, recipe_description, picture, prep_time, cook_time, servings, recipe_image, recipe_video, meal_type)

        return redirect(url_for('apps.myRecipe'))
    flash('Invalid name', category='error')

    return redirect(url_for('apps.myRecipe'))


@apps.route('/singleRecipe/<id>', methods=['GET', 'POST'])
def single_recipe(id):
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    comments = Comment.query.all()
    user = User.query.filter_by(email=recipe.email).first()

    profile_pic = '../static/images/userProfileImages/' + user.profile_image + '.jpg'
    if recipe.recipe_video == '':
        display1 = 'display'
    else:
        display1 = ''
    if request.method == "POST":
        return render_template('singleRecipe.html', recipe=recipe, comments=comments, pic=profile_pic, display1=display1, user=user)
    return render_template('singleRecipe.html', recipe=recipe, comments=comments, pic=profile_pic, display1=display1, user=user)


@apps.route('/recipe/<id>', methods=['GET', 'POST'])
def single_recipe_logged(id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    recipe = Recipe.query.filter_by(recipe_id=id).first()
    comments = Comment.query.all()
    current_user = User.query.filter_by(email=session['email']).first()
    current_user_pic = '../static/images/userProfileImages/' + \
        current_user.profile_image + '.jpg'
    user = User.query.filter_by(email=recipe.email).first()
    user_pic = '../static/images/userProfileImages/' + user.profile_image + '.jpg'

    if is_liked(current_user, recipe):
        like = "Liked"
    else:
        like = "Like"

    if is_disliked(current_user, recipe):
        dislike = "Disliked"
    else:
        dislike = "Dislike"

    if is_following(current_user, user):
        sub = 'Unsubscribe'
    else:
        sub = 'Subscribe'

    if is_saved(recipe.recipe_id, current_user.email):
        save = 'Saved'
    else:
        save = 'Save'

    if recipe.recipe_video == '':
        display1 = 'display'
    else:
        display1 = ''

    recommended = recommendation(recipe)
    if request.method == "POST":
        comment = request.form.get("comment")
        email = session['email']

        if len(comment) > 0:
            add_comment(email, recipe.recipe_id, comment)
        comments = Comment.query.all()

    if recipe.email == g.user.email:
        return render_template('mySingleRecipe.html', recipe=recipe, comments=comments, pic1=user_pic, pic2=current_user_pic, like=like, dislike=dislike, save=save, display1=display1, recommended=recommended, user=user)

    return render_template('singleRecipeLogged.html', recipe=recipe, comments=comments, pic1=user_pic, pic2=current_user_pic, like=like, dislike=dislike, sub=sub, save=save, display1=display1, recommended=recommended, user=user)


@apps.route('/subscribe/<email_r>', methods=['GET', 'POST'])
def subscribe(email_r):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    other_user = User.query.filter_by(email=email_r).first()
    current_user = User.query.filter_by(email=session['email']).first()

    if is_following(current_user, other_user):
        remove_following(current_user, other_user)
    else:
        add_following(current_user, other_user)

    return redirect(url_for('apps.view_profile', email_r=email_r))


@apps.route('recipe/subscribe/<email_r>/<recipe_id>', methods=['GET', 'POST'])
def subscribe_recipe(email_r, recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    other_user = User.query.filter_by(email=email_r).first()
    current_user = User.query.filter_by(email=session['email']).first()
    if is_following(current_user, other_user):
        remove_following(current_user, other_user)
    else:
        add_following(current_user, other_user)

    return redirect(url_for('apps.single_recipe_logged', id=recipe_id))


@apps.route('/like/<recipe_id>', methods=['GET', 'POST'])
def like(recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    user = User.query.filter_by(email=session['email']).first()
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    remove_like(user, recipe) if is_liked(
        user, recipe) else add_like(user, recipe)

    return redirect(url_for('apps.single_recipe_logged', id=recipe_id))


@apps.route('/dislike/<recipe_id>', methods=['GET', 'POST'])
def dislike(recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    user = User.query.filter_by(email=session['email']).first()
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    remove_dislike(user, recipe) if is_disliked(
        user, recipe) else add_dislike(user, recipe)

    return redirect(url_for('apps.single_recipe_logged', id=recipe_id))


@apps.route('/save/<recipe_id>', methods=['GET', 'POST'])
def save_other_recipe(recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    user = User.query.filter_by(email=session['email']).first()
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()

    if is_saved(recipe.recipe_id, user.email):
        unsave_recipe(recipe.recipe_id, user.email)
    else:
        save_recipe(recipe.recipe_id, user.email)

    return redirect(url_for('apps.single_recipe_logged', id=recipe_id))


@apps.route('/saved_recipe', methods=['GET'])
def saved_recipe():
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    recipes = get_saved_recipes(session['email'])

    if len(recipes) == 0:
        return render_template('noSavedRecipe.html', recipes=recipes)

    return render_template('savedRecipe.html', recipes=recipes)


@apps.route('/search_result', methods=['POST'])
def search_result():
    data = request.form.get("search_value")

    search_type = request.form.get("select_type")
    if search_type == "User":
        return render_template('searchUser.html', users=search_users(data))

    return render_template('search.html', recipes=search_recipe(data))


@apps.route('/feeds_page', methods=['GET'])
def feeds_page():

    user = User.query.filter_by(email=session['email']).first()
    recipes = following_recipes(user)

    if user.number_following == 0:
        return render_template('noSubRecipe1.html', recipes=recipes)

    if len(recipes) == 0:
        return render_template('noSubRecipe2.html', recipes=recipes)

    return render_template('feedPage.html', recipes=recipes)


@apps.route('/favourite/<recipe_id>', methods=['GET', 'POST'])
def favourite_recipe(recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    user = User.query.filter_by(email=session['email']).first()
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if is_favourite(user, recipe):
        remove_favourite(user.email, recipe.recipe_id)
    else:
        select_favourite(user.email, recipe.recipe_id)

    return redirect(url_for('apps.my_recipe_detail', id=recipe_id))


@apps.route("/othersfavourite/<email_r>", methods=['GET'])
def view_favourite(email_r):
    if not g.user:
        return redirect(url_for('apps.appLogin'))

    user = User.query.filter_by(email=email_r).first()
    if (user.favourite == -1):
        flash('User has no favourite', category='success')
        return redirect(url_for('apps.view_profile', email_r=email_r))

    return redirect(url_for('apps.single_recipe_logged', id=user.favourite))


@apps.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        email = session['email']
        add_feedback(email, subject, message)
        return redirect(url_for('apps.logged'))
    else:
        return render_template('feedback.html')

@apps.route('/ingredients<recipe_id>', methods=['GET', 'POST'])
def ingredients(recipe_id):
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    ingredients = get_ingredients(recipe_id)
    return render_template('ingredients.html', recipe = recipe, ingredients = ingredients)


@apps.route('/contact')
def contact():
    return render_template('contact.html')

@apps.route('/contact/logged')
def contactLogged():
    if not g.user:
        return redirect(url_for('apps.appLogin'))
    return render_template('contactLogged.html')