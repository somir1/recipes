from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User():
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def make_a_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        results = connectToMySQL('login_schema').query_db(query, data)

        return results

    @classmethod
    def get_users_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        email = connectToMySQL('login_schema').query_db(query, data)

        users = []

        for x in email:
            users.append(User(x))

        return users

    @staticmethod
    def validate_user(data):

        is_valid = True

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 2:
            flash("Your first name should be greater then 2 characters")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        if len(data['password']) < 8:
            flash("Your password needs to be greater then 8 charcaters")
            is_valid = False

        if data['password'] != data['confirmpassword']:
            flash("Your passwords does not match")
            is_valid = False

        if len(User.get_users_email(data)) != 0:
            flash("This email is in use")
            is_valid = False
        
        return is_valid
            

