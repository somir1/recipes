from flask_app.models.logins import User
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.logins import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/createuser', methods = ['POST'])
def make_user():
    if not User.validate_user(request.form):
        return redirect('/')
    else:
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        User.make_a_user(data)
    return redirect('/')

@app.route('/loggedin', methods = ['POST'])
def am_i_loggedin():

    users = User.get_users_email(request.form)
    
    if len(users) != 1:
        flash('The email you have entered does not exist')
        return redirect('/')

    user = users[0]


    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password")
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/dashboard')

# @app.route('/success')
# def success():
#     if 'user_id' not in session:
#         flash("Please log in")
#         return redirect('/')
#     return render_template("yourin.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')