#! /usr/bin/env python3

import requests
import textwrap
from itertools import cycle
import sys

"""
This file handles all of the main visual interface with the prints, and takes the data.
It essentially acts as the main script.
"""


def show_title():  # Title of the program printed, right above the menu
    print("My Recipe Program")
    print()


def show_menu():  # Displays the 8 commands usable by the user in a menu format to produce various results.

    print("COMMAND MENU")
    print("1 - List all categories")
    print("2 - List all meals for categories")
    print("3 - Search meal by name")
    print("4 - Get a random meal")
    print("5 - List all areas")
    print("6 - List all meals for an area")
    print("7 - Display menu")
    print("0 - Exit the application")
    print()


def list_categories(categories):  # lists all categories that you can search through
    if categories is not None:
        print("CATEGORIES")
        for i in range(len(categories)):
            category = categories[i]
            print(" " + category.get_category())
    else:
        print("Technical difficulties, please try again later.", file=sys.stderr)

    print()


def list_meals_by_category(categories):  # Inputs a category, and gets all meals for that category
    lookup_category = input("Enter a category: ")
    print()

    if categories is not None:
        found = False

        for i in range(len(categories)):
            category = categories[i]
            if category.get_category().lower() == lookup_category.lower():
                found = True
                break

        if found:
            meals = requests.get_meals_by_category(lookup_category)
            display_meals(lookup_category, meals)
        else:
            print("Invalid category, please try again.\n", file=sys.stderr)
    else:
        print("Technical difficulties, please try again later.", file=sys.stderr)
        print()


def display_meals(title, meals):
    if meals is not None:
        print(title.upper(), "MEALS")
        for i in range(len(meals)):  # loops through all the meals, and prints the names
            meal = meals[i]
            print(" " + meal.get_meal_name())
    else:
        print("Technical difficulties, please try again later.")

    print()


def search_meal_by_name(name):  # function not actually used, see function search_meal_by_name_extra_credit()

    meal = requests.search_meals_by_name(name)
    print()

    if meal == "NotFound":  # Receives if the meal doesnt exist, and prints it out to error
        print("Hey! That meal doesnt exist!!!\n", file=sys.stderr)
        return

    print(f"Recipe: {meal.get_meal_name()}\n")
    print(f"Instructions:")
    wrapper = textwrap.TextWrapper(width=80)
    wrapped = wrapper.wrap(meal.get_meal_instructions())
    for line in wrapped:
        print(line)

    print()

    ingredients = meal.get_meal_ingredients()
    ingredient_names = list(ingredients.keys())
    ingredient_amounts = list(ingredients.values())

    largest_item_in_names_length = len(max(ingredient_amounts, key=len))

    print("Ingredients:")

    print("Measure" + " " * (largest_item_in_names_length - len("measure")) + "Ingredient")

    print("-" * 80)

    for k, v in zip(ingredient_names, ingredient_amounts):
        to_print = v + " " * (largest_item_in_names_length - len(v) + 1) + " " + k
        print(to_print)

    print()


def random_meal():  # gets a random meal through the random meals api and prints its associated instructions
    meal = requests.get_random_meal()
    print("A random meal was selected just for you!\n")
    print(f"Recipe: {meal.get_meal_name()}\n")
    print(f"Instructions:")
    wrapper = textwrap.TextWrapper(width=80)
    wrapped = wrapper.wrap(meal.get_meal_instructions())
    for line in wrapped:
        print(line)

    print()

    ingredients = meal.get_meal_ingredients()
    ingredient_names = list(ingredients.keys())
    ingredient_amounts = list(ingredients.values())

    largest_item_in_names_length = len(max(ingredient_amounts,
                                           key=len))  # finds the largest item so it can use it to calculate the number of spaces used per line

    if largest_item_in_names_length < len("measure"):
        largest_item_in_names_length = len("measure") + 1  # this is so that the first line is not `MeasureIngredient`

    print("Ingredients:")

    print("Measure" + " " * (largest_item_in_names_length - len("measure") + 1) + "Ingredient")

    print("-" * 80)

    for k, v in zip(ingredient_names, ingredient_amounts):
        to_print = str(v) + " " * (largest_item_in_names_length - len(str(v))) + " " + str(
            k)  # calculates the spaces between the ingredient and measure
        print(to_print)

    print()


def list_all_areas():
    areas = requests.list_areas()
    print("AREAS:")
    print("\n".join([f"  {area.get_area_name()}" for area in areas]))
    print()


def list_all_meals_for_area(area):
    meals = requests.list_meals_for_area(area)

    if meals == "NotFound":  # Receives if the meal doesnt exist, and prints it out to error
        print("Area not found\n", file=sys.stderr)
        return print()

    print()
    print(area.upper() + " MEALS")
    print("\n".join([f"  {meal.get_meal_name()}" for meal in meals]))  # gets the meal name for each of the meals
    print()


def search_meal_by_name_extra_credit(name):
    meal = requests.search_meals_by_name(name)
    print()

    if meal == "NotFound":  # Receives if the meal doesnt exist, and prints it out to error
        print("Hey! That meal doesnt exist!\n", file=sys.stderr)
        return

    print(f"Recipe: {meal.get_meal_name()}\n")
    print(f"Instructions:")
    wrapper = textwrap.TextWrapper(width=80)
    wrapped = wrapper.wrap(meal.get_meal_instructions())
    for line in wrapped:
        print(line)

    print()

    ingredients = meal.get_meal_ingredients()
    ingredient_names = list(ingredients.keys())
    ingredient_amounts = list(ingredients.values())

    ingredient_strings = [f"{v} {k}" for k, v in zip(ingredient_names,
                                                     ingredient_amounts)]  # ['self raising flour 1 1/4 cup', 'coco sugar 1/2 cup', 'cacao 1/3 cup raw', 'baking powder 1 tsp', 'flax eggs 2', 'almond milk 1/2 cup', 'vanilla 1 tsp', 'water 1/2 cup boiling']

    cols = [[], [], []]

    currently_appending = cycle([1, 2, 3])

    for num, i in enumerate(currently_appending):
        cols[i - 1].append(ingredient_strings[num])
        if num == len(ingredient_strings) - 1:
            break

    print("Ingredients:")
    print("-" * 80)  # prints out 80 "-"

    for num, col_1_item in enumerate(cols[0]):  # loops through all of the items, and distributes them between 3 columns
        try:
            col_2_item = cols[1][num]
        except IndexError:
            col_2_item = ""

        try:
            col_3_item = cols[2][num]
        except IndexError:
            col_3_item = ""

        line = ""

        # line length is 78 (closest multiple of 3 to 80), so 26 characters per col

        print(  # prints out the rows in different columns (variable names may have been flipped)
            col_1_item + " " * (26 - len(col_1_item)),
            col_2_item + " " * (26 - len(col_2_item)),
            col_3_item + " " * (26 - len(col_3_item))
        )

    print()


def main():
    show_title()
    show_menu()

    categories = requests.get_categories()

    while True:

        # Essentially a switch statement between the different commands

        command = input("What would you like to do? ")

        print()

        if command == "0":
            print("Thank you for dining with us!")
            exit(0)

        elif command == "1":
            list_categories(categories)

        elif command == "2":
            list_meals_by_category(categories)

        elif command == "3":
            meal_input = input("Enter Meal Name: ")
            search_meal_by_name_extra_credit(meal_input)

        elif command == "4":
            random_meal()

        elif command == "5":
            list_all_areas()

        elif command == "6":
            area_input = input("Enter an Area: ")
            list_all_meals_for_area(area_input)

        elif command == "7":
            show_menu()

        else:
            print("Invalid Input. Please try again.", file=sys.stderr)
            print()
            show_menu()


if __name__ == "__main__":
    main()
