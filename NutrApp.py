'''This is a command-line program that asks for ingredient amount, unit, and name.
Compiles each ingredient in a .txt file named recipe_book.txt.
Queries an ingredient database, pulls nutritional info. for each ingredient.
Prints cumulative nutritional info. to recipe_book.txt.  This version also puts all
ingredients into a list.  The list contains the recipe title, embedded list for each
ingredient that contains nutritional information, and the number of ingredients in
the recipe'''

import sqlite3

def main():
    recipe =[]
    title= input("Enter the recipe title: ")
    servSize= eval(input("Enter the serving size: "))
    recipe_write_dbase(title, servSize)
    recipe.append(title)
    recipe.append(servSize)
    title_write(title, servSize)
    more= 'yes'
    tot_calories= float(0)
    tot_protein= float(0)
    tot_fat= float(0)
    tot_carb= float(0)
    tot_sodium= float(0)
    tot_sugar= float(0)
    tot_sat_fat= float(0)
    tot_cholesterol= float(0)
    while more == 'yes':
        amount = eval(input("Enter amount: "))
        unit = input("Enter the unit(I.E.- cup, tsp); ")
        ingredient = input("Enter the ingredient: ")
        ingredients =[]
        description, calories, protein, fat, carbohydrates, sodium,\
            sugar, sat_fat, cholesterol, convert_wt, convert_num, convert_unit=\
            nutr_grabber(ingredient)
        while description== None:
            print("Ingredient not found in database.  Try again: ")
            ingredient = input("Enter the ingredient: ")
            description, calories, protein, fat, carbohydrates, sodium,\
            sugar, sat_fat, cholesterol, convert_wt, convert_num, convert_unit=\
            nutr_grabber(ingredient)
        else:
            converted_ingr= convert(amount, servSize, unit, calories, protein, fat,\
                                    carbohydrates, sodium, sugar, sat_fat, cholesterol, convert_wt,\
                                    convert_num, convert_unit)
            recipe_id= id_grabber(title)
            ingredient_write_dbase(recipe_id, amount, unit, ingredient, converted_ingr)
            ingredients = [amount, unit, ingredient, converted_ingr]            
            recipe.append(ingredients)
            recipe_write(amount, unit, description)
            tot_calories= tot_calories + converted_ingr[0]
            tot_protein = tot_protein + converted_ingr[1]
            tot_fat = tot_fat + converted_ingr[2]
            tot_carb = tot_carb + converted_ingr[3]
            tot_sodium= tot_sodium + converted_ingr[4]
            tot_sugar= tot_sugar + converted_ingr[5]
            tot_sat_fat= tot_sat_fat + converted_ingr[6]
            tot_cholesterol= tot_cholesterol + converted_ingr[7]
            more = input("More ingredients? (Enter 'yes' or 'no'):")
            while more != 'yes' and more != 'no':
                print("You must enter either 'yes' or 'no'.  Try again...")
                more = input("More ingredients? (Enter 'yes' or 'no'):") 
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, tot_sat_fat, tot_cholesterol)
    num_ingr = len(recipe)-1
    recipe.append(num_ingr)

'''Submits the ingredient name and returns the nutritional information.'''
def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDAData.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, FA_Sat_g,Cholestrl_mg, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg, Gm_unit, num, unit from USDADataProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protein= row[2]
                fat= row[3]
                carbohydrates= row[4]
                sodium= row[12]
                sugar= row[6]
                Sat_fat= row[7]
                Cholesterol= row[8]
                convert_wt= row[13]
                convert_num= row[14]
                convert_unit= row[15]

                
            else:
                description = None
                calories= None
                protein= None
                fat= None
                carbohydrates= None
                sodium= None
                sugar= None
                Sat_fat= None
                Cholesterol= None
                convert_wt= None
                convert_num= None
                convert_unit= None
        finally:
            c.close()

    finally:
        conn.close()

    return description, calories, protein, fat, carbohydrates, sodium, sugar, Sat_fat, Cholesterol, convert_wt, convert_num, convert_unit

#prints title of recipe to recipe_book.txt
def title_write(title, servSize):
    recipe= open("recipe_book.txt", "a")
    print (title, file=recipe)
    print ("Serves: ", servSize, file=recipe)
    recipe.close()

#prints amount, unit, and ingredient to recipe_book.txt
def recipe_write(amount, unit, description):
    recipe= open("recipe_book.txt", "a")
    print (amount,' ', unit,' ',description, file=recipe)
    recipe.close()

#prints nutritional information to recipe_book.txt
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, Sat_fat, Cholesterol):
    recipe= open("recipe_book.txt", "a")
    print ("Nutritional information", file=recipe)
    print ("calories: ",round(tot_calories,0), file=recipe)
    print ("Protein: ", round(tot_protein, 2),' gm', file=recipe)
    print ("Fat: ", round(tot_fat, 2), ' gm', file=recipe)
    print ("Carbohydrates: ", round(tot_carb, 2),' gm', file=recipe)
    print ("Sodium: ", round(tot_sodium, 2),' mg', file=recipe)
    print ("Sugar: ", round(tot_sugar, 2),' gm', file=recipe)
    print ("Saturated fat: ", round(Sat_fat, 2),' gm', file=recipe)
    print ("Cholesterol: ", round(Cholesterol, 2), ' gm', file=recipe)
    recipe.close()
    
'''This function converts the nutritional values for each nutrient in each
ingredient from per 100 gm to what ever is called for in the recipe.
For example, coverts nutritional information for 100 gms of flour to nutritional
information for 2 sups flour.  If needed, units (cup, tsp, tbsp) are converted into
whatever is the most common unit for that ingredient.  For example, a recipe gives
the flour amount in tbsp, this will be converted into cups (the most commonly
used unit to measure flour).'''
def convert(amount, servSize, unit, calories, protein, fat, carbohydrates, sodium, sugar, sat_fat\
            , cholesterol, convert_wt, convert_num, convert_unit):
    #Convert factors
    convert_val = {'cuptsp': 48.0, 'tspcup': 1/48.0, 'cuptbsp': 16.0, 'tsptbsp': 1/3.0, \
                   'tbsptsp': 3.0, 'ozcup': 1/8.0, 'oztbsp': 0.5, 'tbspoz': 2.0, \
                   'cupoz': 8.0, 'ozlb': 1/16.0, 'lboz': 16.0}
   
    ing_list= [float(calories), float(protein), float(fat), float(carbohydrates)\
               , float(sodium), float(sugar), float(sat_fat), float(cholesterol)]
   
    convert_val= float
    convert_wt= float(convert_wt)
    convert_num = float(convert_num)
    converted_ing= []

    if unit == convert_unit:
   
        convert_wt = (convert_wt/convert_num) * amount
        convert_val = convert_wt / 100
       
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing
   
    else:
        val = unit + convert_unit
        amount = amount * convert_val[val]

        convert_wt = (convert_wt/convert_num) * amount
        convert_val = convert_wt / 100
           
        for i in ing_list:
            i = i * convert_val[val]
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

'''The following functions write recipe information to two separate databases,
recipe.sqlite and ingredients.sqlite.'''

#adds recipe title and generates recipe_id.
def recipe_write_dbase(title, servSize):
    conn= sqlite3.connect("recipe.sqlite")
    try:
        c= conn.cursor()
        try:
            c.execute("INSERT INTO recipe (recipe_title, servSize) VALUES (?, ?)", (title, servSize,))
            conn.commit()

        finally:
            c.close()

    finally:
        conn.close()

#Grabs recipe_id to be used as key for ingredients.
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

#Writes ingredients to ingredients.sqlite.  Also adds recipe_id so ingredients can
#be retrieved.
def ingredient_write_dbase(recipe_id, amount, unit, ingredient, converted_ingr):
    calories, protein, fat, carbohydrates, sodium, sugar, sat_fat, cholesterol= converted_ingr
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c=conn.cursor()
        try:
            c.execute("INSERT INTO ingredient (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar, sat_fat, cholesterol)\
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar, sat_fat, cholesterol))
            conn.commit()
        finally:
            c.close()
    finally:
        conn.close()

    
main()
