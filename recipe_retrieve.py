#! /usr/bin/python

'''Compiles recipes from ingredient and recipe databases.'''

import sqlite3

def main():

    recipe= input("What recipe would you like?- ")
    recipe_id= id_grabber(recipe)
    
def id_grabber(recipe):
    conn= sqlite3.connect("recipe.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("SELECT recipe_id FROM recipe where recipe_title = ?", (recipe,))

            row= c.fetchone()
            if row:
                recipe_id= row[0]
            else:
                recipe_id= None
        finally:
            c.close()

    finally:
        conn.close()

    return recipe_id

def get_ingredients(recipe_id):
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("Select * from ingredient where recipe_id = ?", (recipe_id,))
            #research this, probably does not use fetchone()
            row = c.fetchone()
            if row:
                


def compile_recipe():
    pass

def print_recipe():
    pass

main()
