import sqlite3
'''This script contains the functions for writing recipes' contents to a database for later retrieval.
This uses two sqlite databases, recipe.sqlite and ingredients.sqlite.

This code will eventually be incorporated into nutr_app.py''' 

def main():
    title= input("Enter recipe title: ")
    recipe_write_dbase(title)
    recipe_id= id_grabber(title)
    print (recipe_id)
    
'''Opens recipe.sqlite, writes recipe title and databse generates recipe_id.   '''
def recipe_write_dbase(title):
    conn= sqlite3.connect("recipe.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("INSERT INTO recipe (recipe_title) VALUES (?)", (title,))
            conn.commit()

        finally:
            c.close()

    finally:
        conn.close()

'''Returns recipe_id to be used to link specific ingredients with a recipe.'''
def id_grabber(title):
    conn= sqlite3.connect("recipe.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("SELECT recipe_id FROM recipe where recipe_title = ?", (title,))

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

'''Will write ingredient specifics to ingredients.sqlite (not created yet).
Each ingredient has the recipe_id attached for later retrieval and compiling.'''
'''def ingredient_write_dbase(index, amount, unit, converted_ingr):
    conn=sqlite3.connect("recipe.sqlite")
    try:
        c=conn.cursor()
        try:
            c.execute("SELECT FROM recipe'''


main()
