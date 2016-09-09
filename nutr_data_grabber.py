import sqlite3

def main():
    ingredient = input("Enter the ingredient: ")
    if ingredient:
        description, calories, protein, total_fat, carbohydrates= nutr_grabber(ingredient)
        print (description)
        print (calories)
        print (protein)
        print (total_fat)
        print (carbohydrates)

def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDADataProto.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg from FoodDatabaseProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[1]
                calories= row[3]
                protein= row[4]
                total_fat= row[5]
                carbohydrates= row[7]
            else:
                description = None
                calories= None
                protein= None
                total_fat= None
                carbohydrates= None

        finally:
            c.close()

    finally:
        conn.close()

    return description, calories, protein, total_fat, carbohydrates

main()
