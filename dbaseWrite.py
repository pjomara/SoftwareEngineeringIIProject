import sqlite3

def main():
    title= input("Enter recipe title: ")
    recipe_write_dbase(title)
    recipe_id= id_grabber(title)
    print (recipe_id)
    

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

def ingredient_write_dbase(recipe_id, amount, unit, converted_ingr):
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c=conn.cursor()
        try:
            c.execute("INSERT INTO ingredients (recipe_id, amount, unit, converted_ingr)\
                      VALUES (?, ?, ?, ?)", (recipe_id, amount, unit, converted_ing,))
            conn.commit()
        finally:
            c.close()
    finally:
        conn.close()





main()
