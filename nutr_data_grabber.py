'''This is a command-line program that asks for ingredient amount, unit, and name.
Compiles each ingredient in a .txt fiel named recipe_book.txt.
Queries an ingredient database, pulls nutritional info. for each ingredient.
Prints cumulative nutritional info. to recipe_book.txt.'''

import sqlite3

def main():
    title= input("Enter the recipe title: ")
    title_write(title)
    more= 'yes'
    tot_calories= float(0)
    tot_protein= float(0)
    tot_fat= float(0)
    tot_carb= float(0)
    while more == 'yes':
        amount = eval(input("Enter amount: "))
        unit = input("Enter the unit(I.E.- cup, tsp); ")
        ingredient = input("Enter the ingredient: ")
        if ingredient:
            description, calories, protein, total_fat, carbohydrates= nutr_grabber(ingredient)
            recipe_write(amount, unit, description)
            tot_calories= tot_calories + float(calories)
            tot_protein = tot_protein + float(protein)
            tot_fat = tot_fat + float(total_fat)
            tot_carb = tot_carb + float(carbohydrates)
            more = input("More ingredients? (Enter 'yes' or 'no'):")
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb)

def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDADataProto.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg from FoodDatabaseProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protein= row[2]
                total_fat= row[3]
                carbohydrates= row[4]
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

#prints title of recipe to recipe_book.txt
def title_write(title):
    recipe= open("recipe_book.txt", "a")
    print (title, file=recipe)
    recipe.close()

#prints amount, unit, and ingredient to recipe_book.txt
def recipe_write(amount, unit, description):
    recipe= open("recipe_book.txt", "a")
    print (amount,' ', unit,' ',description, file=recipe)
    recipe.close()

#prints nutritional information to recipe_book.txt
#as of 9/13/2016- prints per 100g for each ingredient.- This needs to be fixed    
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb):
    recipe= open("recipe_book.txt", "a")
    print ("\n","Nutritional information", file=recipe)
    print ("calories: ",round(tot_calories,2), file=recipe)
    print ("Protein: ", round(tot_protein, 2), file=recipe)
    print ("Fat: ", round(tot_fat, 2), file=recipe)
    print ("Carbohydrates: ", round(tot_carb, 2), file=recipe)
    recipe.close()

# cal_converter converts calories from per 100g to recipe amount. 
def cal_converter():
    pass

#prot_converter converts protien from per 100 g to recipe amount.
def prot_converter():
    pass

#fat_converter converts fat from per 100g to recipe amount.
def fat_converter():
    pass

#carb_converter converts carbs from per 100g to recipe amount.
def carb_converter():
    pass

main()
