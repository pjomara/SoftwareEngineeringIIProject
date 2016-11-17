#! /usr/bin/python

'''Compiles recipes from ingredient and recipe databases.'''

import sqlite3

def main():

    recipe= input("What recipe would you like?- ")
    recipe_id, title, servSize= id_grabber(recipe)
    ingredients= get_ingredients(recipe_id)
    print_recipe(title, servSize, ingredients)
    print_nutrition(ingredients)
    
    
def id_grabber(recipe):
    conn= sqlite3.connect("recipe.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("SELECT * FROM recipe where recipe_title = ?", (recipe,))

            row= c.fetchone()
            if row:
                recipe_id= row[0]
                title= row[1]
                servSize= row[2]
            else:
                recipe_id= None
        finally:
            c.close()

    finally:
        conn.close()

    return recipe_id, title, servSize

def get_ingredients(recipe_id):
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("Select * from ingredient where recipe_id = ?", (recipe_id,))
            ingredients = c.fetchall()
        finally:
            c.close()

    finally:
        conn.close()

    return ingredients
 

def print_recipe(title, servSize, ingredients):
    print (title)
    print ("Serves: ", servSize)
    print ("Ingredients:")
    print_ingredients(ingredients)
    
def print_ingredients(ingredients):
    for i in ingredients:
        print (i[1], " ",i[2]," ",i[3])

def print_nutrition(ingredients):
    calories= 0
    protein= 0
    fat= 0
    carbohydrates= 0
    sodium= 0
    sugar= 0
    sat_fat= 0
    cholesterol= 0
    for i in ingredients:
        calories= calories + i[4]
        protein= protein + i[5]
        fat= fat + i[6]
        carbohydrates= carbohydrates + i[7]
        sodium = sodium + i[8]
        sugar= sugar + i[9]
        sat_fat= sat_fat + i[10]
        cholesterol= cholesterol + i[11]
    print ("\nNutritional information")
    print("Calories: ", calories)
    print("Protein: ", protein, " gm")
    print("Fat: ", fat, " gm")
    print("Carbohydrates: ", carbohydrates, " gm")
    print("Sodium: ", sodium, " mg")
    print("Sugar: ", round(sugar,2), " gm")
    print("Saturated fat: ", sat_fat, " gm")
    print("Cholesterol: ", cholesterol, " mg")

main()
