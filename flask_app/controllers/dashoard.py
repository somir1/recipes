from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.logins import User
from flask_app.models.recipe import Recipe


@app.route('/dashboard')
def index():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    recipes = Recipe.get_all_recipe()
    return render_template("yourin.html", recipes = recipes)

@app.route('/create/recipe')
def create_recipe():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    return render_template("create.html")

@app.route('/new/recipe', methods = ['POST'])
def insert_recipe():
    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'unders30': request.form['unders30'],
            'date': request.form['date'],
            'users_id': session['user_id']
        }

        Recipe.make_recipe(data)
        return redirect("/dashboard")
    return redirect("/create/recipe")

@app.route('/show/<int:recipe_id>')
def show_recipe(recipe_id):

    data = {
        'id': recipe_id
    }

    recipe = Recipe.get_recipes_by_id(data)
    print("something is wrong ")

    print(recipe)
    return render_template("showrecipe.html", recipe = recipe)

@app.route('/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }

    recipe = Recipe.get_recipes_by_id(data)

    return render_template('edit.html', recipe = recipe)

@app.route('/update/recipe/<int:recipe_id>', methods = ['POST'])
def update_recipe(recipe_id):

    data = {
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'unders30': request.form['unders30']
    }

    print(data)

    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    data = {
        'id' : recipe_id
    }

    Recipe.delete(data)
    return redirect('/dashboard')
