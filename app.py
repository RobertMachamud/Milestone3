
import os
import random
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checking if username already exist in db
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if user_exists:
            flash("Sorry, this Username is already taken")
            return redirect(url_for("register"))

        register = {
            "name": request.form.get("name").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email"),
            "level": request.form.get("level"),
            "dob": request.form.get("dob"),
            "about": request.form.get("about"),
            "profile_img": "chef_profile.png",
            "own_recipes": 0,
            "saved_recipes": []
        }

        mongo.db.users.insert_one(register)

        # putting new user into session cookie
        session["user"] = request.form.get("username").lower()
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # checking if username in db
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user_exists:
            # checking if password is matching user input
            if check_password_hash(
                    user_exists["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # flash()
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Username and/or Password incorrect")
                return redirect(url_for("login"))

        else:
            # in case username doesn't exists
            flash("Username and/or Password incorrect")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # removing user from sessions cookies
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # use session user's username from db
    user = mongo.db.users.find_one(
        {"username": session["user"]}
    )

    username = user["username"]
    if session["user"]:
        return render_template("profile.html", username=username, user=user)

    return redirect(url_for("login"))


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    username = user["username"]

    if request.method == "POST":
        edit = {
            "name": request.form.get("edit_name").lower(),
            "username": request.form.get("edit_username").lower(),
            "password": user["password"],
            "email": request.form.get("edit_email"),
            "level": request.form.get("edit_level"),
            "dob": request.form.get("edit_dob"),
            "about": request.form.get("edit_about"),
            "profile_img": "chef_profile.png"
        }
        edit["own_recipes"] = user["own_recipes"]
        edit["saved_recipes"] = user["saved_recipes"]

        if len(request.form.get("edit_password")) >= 5:
            edit["password"] = generate_password_hash(
                request.form.get("edit_password"))

        mongo.db.users.update({"_id": ObjectId(user_id)}, edit)
        flash("User Updated")
        redirect(url_for("profile", username=username))

    return render_template("edit_profile.html", user=user)


@app.route("/recipes")
def recipes():
    recipes = list(mongo.db.recipes.find())
    categories = list(mongo.db.categories.find())
    return render_template("recipes.html", recipes=recipes,
                           categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    categories = list(mongo.db.categories.find())
    return render_template("recipes.html", recipes=recipes,
                           categories=categories)


@app.route("/clicked-recipe/<recipe_id>")
def clicked_recipe(recipe_id):
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]}
        )
        if recipe_id not in user["saved_recipes"]:
            button_txt = "Save Recipe"
        else:
            button_txt = "Unsave Recipe"
    else:
        button_txt = "Save Recipe"

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        "clicked_recipe.html", recipe=recipe, button_txt=button_txt)


@app.route("/save_recipe/<recipe_id>", methods=["GET", "POST"])
def save_recipe(recipe_id):
    user = mongo.db.users.find_one(
        {"username": session["user"]}
    )
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if recipe_id not in user["saved_recipes"]:
        mongo.db.users.update(
            {"_id": user["_id"]},
            {"$push": {"saved_recipes": recipe_id}}
        )
        button_txt = "Unsave Recipe"
        flash("Recipe Saved")
    else:
        mongo.db.users.update(
            {"_id": user["_id"]},
            {"$pull": {"saved_recipes": recipe_id}}
        )
        button_txt = "Save Recipe"
        flash("Recipe Unsaved")
    return render_template(
        "clicked_recipe.html", recipe=recipe, button_txt=button_txt)


@app.route("/saved_recipes")
def saved_recipes():
    saved_recipes = []
    user = mongo.db.users.find_one(
        {"username": session["user"]}
    )

    for id in user["saved_recipes"]:
        retrieved_saved_recipe = mongo.db.recipes.find_one(
            {"_id": ObjectId(id)})
        saved_recipes.append(retrieved_saved_recipe)

    return render_template("saved_recipes.html", saved_recipes=saved_recipes)


@app.route("/my_recipes")
def my_recipes():
    my_recipes = list(mongo.db.recipes.find(
                                    {"created_by": session["user"]}))
    return render_template("my_recipes.html", my_recipes=my_recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():

    if request.method == "POST":
        ingredient_count = 0
        prep_step_count = 1
        ingredients = []
        prep_steps = []

        while True:
            if f'recipe_ingredient_{ingredient_count}' in request.form:
                ingredient = {
                    "amount": request.form.get(
                        f'recipe_amount_{ingredient_count}'),
                    "unit": request.form.get(
                        f'recipe_unit_{ingredient_count}'),
                    "ingredient": request.form.get(
                        f'recipe_ingredient_{ingredient_count}'),
                }
                ingredients.append(ingredient)
                ingredient_count += 1
            else:
                break

        while True:
            if f'prep_step_{prep_step_count}' in request.form:
                prep_step = {
                    "step": request.form.get(
                        f'prep_step_{prep_step_count}')
                }
                prep_steps.append(prep_step)
                prep_step_count += 1
            else:
                break

        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "difficulty": request.form.get("difficulty"),
            "persons": request.form.get("persons"),
            "ingredients": ingredients,
            "duration_h": request.form.get("duration_h"),
            "duration_min": request.form.get("duration_min"),
            "prep_steps": prep_steps,
            "category": request.form.get("category"),
            "recipe_img": request.form.get("recipe_img"),
            "created_by": session["user"],
            "rating": random.randint(0, 5)
        }

        if len(request.form.get("recipe_img")) < 1:
            recipe["recipe_img"] = "pexels-any-lane-5945747.jpg"

        user = mongo.db.users.find_one(
            {"username": session["user"]}
        )
        mongo.db.users.update(
            {"_id": user["_id"]},
            {"$inc": {"own_recipes": 1}}
        )
        mongo.db.recipes.insert_one(recipe)
        flash("Thank You for sharing your Recipe!")
        redirect(url_for("recipes"))

    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = list(mongo.db.categories.find())

    if request.method == "POST":
        ingredient_count = 0
        prep_step_count = 1
        ingredients = []
        prep_steps = []

        while True:
            if f'recipe_ingredient_{ingredient_count}' in request.form:
                ingredient = {
                    "amount": request.form.get(
                        f'recipe_amount_{ingredient_count}'),
                    "unit": request.form.get(
                        f'recipe_unit_{ingredient_count}'),
                    "ingredient": request.form.get(
                        f'recipe_ingredient_{ingredient_count}'),
                }
                ingredients.append(ingredient)
                ingredient_count += 1
            else:
                break

        while True:
            if f'prep_step_{prep_step_count}' in request.form:
                prep_step = {
                    "step": request.form.get(
                        f'prep_step_{prep_step_count}')
                }
                prep_steps.append(prep_step)
                prep_step_count += 1
            else:
                break

        updated_recipe = {
            "recipe_name": request.form.get("edit_recipe_name"),
            "difficulty": request.form.get("difficulty"),
            "persons": request.form.get("persons"),
            "ingredients": ingredients,
            "duration_h": request.form.get("edit_duration_h"),
            "duration_min": request.form.get("edit_duration_min"),
            "prep_steps": prep_steps,
            "category": request.form.get("category"),
            "recipe_img": request.form.get("recipe_img"),
            "created_by": recipe["created_by"],
            "rating": recipe["rating"]
        }
        mongo.db.recipes.update({"_id": ObjectId(
            recipe_id)}, updated_recipe)
        return redirect(url_for("my_recipes"))

    return render_template(
        "edit_recipe.html", categories=categories, recipe=recipe)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    user = mongo.db.users.find_one(
        {"username": session["user"]}
    )
    mongo.db.users.update(
        {"_id": user["_id"]},
        {"$inc": {"own_recipes": -1}}
    )
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Your Recipe Is Deleted")
    return redirect(url_for("my_recipes"))


@app.route("/categories")
def categories():
    categories = list(mongo.db.categories.find())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "category_png": request.form.get("category_png")
        }
        mongo.db.categories.insert_one(category)
        flash("You have added a new category")
        return redirect(url_for("categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        to_submit = {
            "category_name": request.form.get("category_name"),
            "category_png": request.form.get("category_png")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, to_submit)
        flash("You have updated a category")
        return redirect(url_for("categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("You have deleted a category")
    return redirect(url_for("categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
