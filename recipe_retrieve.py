#! /usr/bin/python

'''Compiles recipes from ingredient and recipe databases.'''

import sqlite3

def main():

    recipe= input("What recipe would you like?- ")
    recipe_id, title, servSize= id_grabber(recipe)
    ingredients= get_ingredients(recipe_id)
    print_recipe(title, servSize, ingredients)
    
    
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
            if ingredients:
                ingredients.append(len(ingredients))
            else:
                ingredients= None
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
        print(i[1], " ",i[2]," ",i[3])

main()
