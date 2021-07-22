from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.logins import User

class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.unders30 = data['unders30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def make_recipe(cls, data):
        query = "INSERT INTO recipes (name, unders30, description, instructions, date, users_id) VALUES (%(name)s, %(unders30)s, %(description)s, %(instructions)s, %(date)s, %(users_id)s);"

        results = connectToMySQL('login_schema').query_db(query, data)

        return results

    @classmethod
    def get_all_recipe(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.users_id = users.id"

        results = connectToMySQL('login_schema').query_db(query)
        
        recipes = []

        for item in results:
            recipe = cls(item)
            user = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            recipe.user = User(user)
            recipes.append(recipe)

        return recipes

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, unders30 = %(unders30)s WHERE id = %(id)s;'
        return connectToMySQL('login_schema').query_db(query, data)
        

    @classmethod
    def get_recipes_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"

        results = connectToMySQL('login_schema').query_db(query, data)
        print(results)
        # recipe = results[0]
        # user = {
        #     'id' : results[0]['users.id'],
        #     'first_name' : results[0]['first_name'],
        #     'last_name' : results[0]['last_name'],
        #     'email' : results[0]['email'],
        #     'password' : results[0]['password'],
        #     'created_at': results[0]['users.created_at'],
        #     'updated_at': results[0]['users.updated_at']
        # }

        recipe_obj = {
            'id' : results[0]['id'],
            'name': results[0]['name'],
            'unders30' : results[0]['unders30'],
            'description' : results[0]['description'],
            'instructions' : results[0]['instructions'],
            'date' : results[0]['date'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at'],
            'users_id' : results[0]['users_id']
        }

        recipe = Recipe(recipe_obj)
        
        return recipe

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL('login_schema').query_db(query, data)

    

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3 or len(data['name']) > 80:
            flash("The name of the recipe should be between 3 to 80 characters.")
            is_valid = False

        if len(data['description']) < 3 or len(data['description']) > 800:
            flash("The description must be between 3 to 800 characters.")
            is_valid = False

        if len(data['instructions']) < 3:
            flash("The instruction must be greater then 3 characters.")

        if len(data['date']) == 0:
            flash("Please input a valid date.")
            is_valid = False

        return is_valid

