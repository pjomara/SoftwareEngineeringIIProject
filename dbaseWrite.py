import sqlite3

def main():
    title= input("Enter recipe title: ")
    recipe_write_dbase(title)

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

main()
