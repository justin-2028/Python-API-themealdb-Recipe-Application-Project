from urllib import request, parse
import json

from objects import Category, Meal, Area

"""
This is where all of the requests to the meal API are made.
It then returns this data to be printed by main.py in the form of objects (see objects.py for more)
This file mostly carries the code similarly among functions, so the comments are minimal. 
"""

def get_categories():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
    f = request.urlopen(url) # makes the request, simple as that
    categories = []

    try:
        data = json.loads(f.read().decode('utf-8')) # converts the data to JSON
        for category_data in data['meals']: # loops through all the categories returned from the API, and appends them
            category = Category(category_data['strCategory'])

            categories.append(category)

    except(ValueError, KeyError, TypeError): # makes sure that if the API makes an error, it will be handled
        return None

    return categories


def get_meals_by_category(category):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + category
    f = request.urlopen(url)
    meals = []

    try:
        data = json.loads(f.read().decode('utf-8'))
        for meal_data in data['meals']:
            meal = Meal(meal_data['strMeal'])

            meals.append(meal)

    except(ValueError, KeyError, TypeError):
        return None

    return meals


def search_meals_by_name(category):
    category = category.replace(" ", "%20")
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + category
    f = request.urlopen(url)

    try:
        data = json.loads(f.read().decode('utf-8'))

        if data["meals"] is None: # tells main.py that the meal was not found, so it can print it to sys.stderr
            return "NotFound"

        meal_data = data["meals"][0]

        ingredients = {}

        for i in range(1, 20+1):
            if meal_data[f"strIngredient{i}"] == "":
                break
            ingredients[meal_data[f"strIngredient{i}"]] = meal_data[f"strMeasure{i}"]

        meal = Meal(name=meal_data["strMeal"], instructions=meal_data["strInstructions"], ingredients=ingredients)

        return meal

    except(ValueError, KeyError, TypeError):
        return None

def get_random_meal():
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    f = request.urlopen(url)

    try:
        data = json.loads(f.read().decode('utf-8'))
        meal_data = data["meals"][0]

        ingredients = {}

        for i in range(1, 20+1): # loops through all the ingredients, and creates a dictionary of {strIngredient: strMeasure}
            if meal_data[f"strIngredient{i}"] == "":
                break
            ingredients[meal_data[f"strIngredient{i}"]] = meal_data[f"strMeasure{i}"]

        meal = Meal(name=meal_data["strMeal"], instructions=meal_data["strInstructions"], ingredients=ingredients)

        return meal



    except(ValueError, KeyError, TypeError):
        return None

def list_areas():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    f = request.urlopen(url)




    try:
        data = json.loads(f.read().decode('utf-8'))
        areas = [Area(i['strArea']) for i in data["meals"]]

        return areas
        



    except(ValueError, KeyError, TypeError):
        return None
    
def list_meals_for_area(area):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?a=" + area
    f = request.urlopen(url)

    try:
        data = json.loads(f.read().decode('utf-8'))
        if data["meals"] is None: # tells main.py that the meal was not found, so it can print it to sys.stderr
            return "NotFound"
        
        meals = [Meal(name=i['strMeal']) for i in data["meals"]] # Converts JSON data to easily
        # readable and workable Meal objects, in one simple line!

        return meals

    except(ValueError, KeyError, TypeError):
        return None
