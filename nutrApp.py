'''This is a command-line program that asks for ingredient amount, unit, and name.
Compiles each ingredient in a .txt file named recipe_book.txt.
Queries an ingredient database, pulls nutritional info. for each ingredient.
Prints cumulative nutritional info. to recipe_book.txt.  This version also puts all
ingredients into a list.  The list contains the recipe title, embedded list for each
ingredient that contains nutritional information, and the number of ingredients in
the recipe'''

import sqlite3

def main():
    """Opens a list called recipe"""
    recipe =[]
    """Gets the recipe name and serving size and writes them to recipe"""
    title= input("Enter the recipe title: ")
    """Error checking for the serving size"""
    try:
        servSize= int(input("Enter the serving size: "))
    except ValueError:
        print("You must enter an integer.  Try again.")
        servSize= eval(input("Enter the serving size: "))
    recipe_write_dbase(title, servSize)
    recipe.append(title)
    recipe.append(servSize)
    title_write(title, servSize)
    """Set default values for variables. More is used to determine if the user wants to input more ingredients"""
    more= 'yes'
    tot_calories= float(0)
    tot_protein= float(0)
    tot_fat= float(0)
    tot_carb= float(0)
    tot_sodium= float(0)
    tot_sugar= float(0)
    tot_sat_fat= float(0)
    tot_cholesterol= float(0)
    """Keeps taking ingredients from the user as long as they keep entering yes for more"""
    while more == 'yes':
        """Error checking for ingredient amount"""
        try:
            amount = int(input("Enter amount: "))
        except ValueError:
            print("You must enter an integer.  Try again.")
            amount = int(input("Enter amount: "))
        """Error checking for the unit"""
        unit = input("Enter the unit(I.E.- cup, tsp); ")
        while unit !="cup" and unit !="tsp" and unit !="oz" and unit !="tbsp":
            print("Accepted units are 'cup', 'tsp', 'tbsp', or 'oz'.  Try again'")
            unit = input("Enter the unit(I.E.- cup, tsp); ")
        else:
            ingredient = input("Enter the ingredient: ")
            ingredients =[]
            description, calories, protein, fat, carbohydrates, sodium,\
                sugar, sat_fat, cholesterol, convert_wt, convert_num, convert_unit=\
                nutr_grabber(ingredient)
            while description== None:
                """Error checking for ingredient name"""
                print("Ingredient not found in database.  Try again: ")
                ingredient = input("Enter the ingredient: ")
                description, calories, protein, fat, carbohydrates, sodium,\
                sugar, sat_fat, cholesterol, convert_wt, convert_num, convert_unit=\
                """Grabs the nutrition information from the database"""
                nutr_grabber(ingredient)
        """If the ingredient doesn't have a description, an error is returned saying
        that the ingredient isn't in the database"""
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
            """Sets recipe_id to be used as a key"""
            recipe_id= id_grabber(title)
            """Writes the key and nutrition information to the database"""
            ingredient_write_dbase(recipe_id, amount, unit, ingredient, converted_ingr)
            ingredients = [amount, unit, ingredient, converted_ingr]
            """Appends the ingredients to the recipe"""
            recipe.append(ingredients)
            """Writes amount, unit, and ingredient to recipe_book.txt"""
            recipe_write(amount, unit, description)
            """Calculates the total values for each nutritional category"""
            tot_calories= tot_calories + converted_ingr[0]
            tot_protein = tot_protein + converted_ingr[1]
            tot_fat = tot_fat + converted_ingr[2]
            tot_carb = tot_carb + converted_ingr[3]
            tot_sodium= tot_sodium + converted_ingr[4]
            tot_sugar= tot_sugar + converted_ingr[5]
            tot_sat_fat= tot_sat_fat + converted_ingr[6]
            tot_cholesterol= tot_cholesterol + converted_ingr[7]
            more = input("More ingredients? (Enter 'yes' or 'no'):")
            """Error checking to make sure that the user enters 'yes' or 'no' for more ingredients"""
            while more != 'yes' and more != 'no':
                print("You must enter either 'yes' or 'no'.  Try again...")
                more = input("More ingredients? (Enter 'yes' or 'no'):")    
    """Writes the nutrition label given the nutrition information"""       
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, tot_sat_fat, tot_cholesterol, servSize)
    num_ingr = len(recipe)-1
    """Appends onto the recipe the number of ingredients"""
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

"""Prints title of recipe to recipe_book.txt"""
def title_write(title, servSize):
    recipe= open("recipe_book.txt", "a")
    print (title, file=recipe)
    """Prints the Serving Size"""
    print ("Serves: ", servSize, file=recipe)
    recipe.close()

"""Prints amount, unit, and ingredient to recipe_book.txt"""
def recipe_write(amount, unit, description):
    recipe= open("recipe_book.txt", "a")
    print (amount,' ', unit,' ',description, file=recipe)
    recipe.close()

"""Prints nutritional label to recipe_book.txt"""
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, Sat_fat, Cholesterol, servSize):

    tot_ft_dv =65.0
    tot_chol_dv =300.0
    tot_sod_dv =2400.0
    tot_carb_dv =300.0
    tot_prot_dv =50.0

    ft_dv= (tot_fat/tot_ft_dv)*100
    chol_dv= (Cholesterol/tot_chol_dv)*100
    sod_dv= (tot_sodium/tot_sod_dv)*100
    carb_dv= (tot_carb/tot_carb_dv)*100
    prot_dv= (tot_protein/tot_prot_dv)*100
    sod_dv= (tot_sodium/tot_sod_dv)*100
    
    """Opens recipe_book.txt to write the label"""
    recipe= open("recipe_book.txt", "a")

    """Format for the nutrition label"""
    print ("_______________________________", file=recipe)
    print ("Nutrition Facts", file=recipe)
    print ("_______________________________", file=recipe)
    print ("Serving Size ", int(servSize), file=recipe)
    print ("_______________________________", file=recipe)
    print ("Calories ", int(tot_calories), file=recipe)
    print ("_______________________________", file=recipe)
    print ("                 % Daily Value*", file=recipe)
    print ("_______________________________", file=recipe)
    print ("Total Fat ", int(tot_fat), "g          ", int(ft_dv),"%", file=recipe)
    print ("_______________________________", file=recipe)
    print ("   Saturated Fat ", int(Sat_fat), "g",  file=recipe)
    print ("_______________________________", file=recipe)
    print ("Cholesterol ", int(Cholesterol), "mg         ", int(chol_dv), "%", file=recipe)
    print ("_______________________________", file=recipe)
    print ("Sodium ", int(tot_sodium), "mg           ", int(sod_dv), "%", file=recipe)
    print ("_______________________________", file=recipe)
    print ("Carbohydrates ", int(tot_carb), "g      ", int(carb_dv), "%", file=recipe)
    print ("_______________________________", file=recipe)
    print ("   Sugars ", int(tot_sugar), "g", file=recipe)
    print ("_______________________________", file=recipe)
    print ("Protein ", int(tot_protein), "g             ", int(prot_dv), "%", file=recipe)
    print ("_______________________________", file=recipe)
    print ("*Daily value percentages are ", file=recipe)
    print ("based on a 2,000 calorie diet ", file=recipe)
    print ("_______________________________", file=recipe)
    print ("\n", file=recipe)
    recipe.close()
    
"""Converts nutrition information for each ingredient from 100g default value to whatever value
   is needed for the recipe"""
def convert(amount, servSize, unit, calories, protein, fat, carbohydrates, sodium, sugar, sat_fat\
            , cholesterol, convert_wt, convert_num, convert_unit):
    """Convert factors"""
    convert_val = {'cuptsp': 48.0, 'tspcup': 0.02083, 'cuptbsp': 16.0, 'tsptbsp': 0.333, \
                   'tbspcup': 0.0625, 'tbsptsp': 3.0, 'ozcup': 0.125, 'oztbsp': 0.5, 'tbspoz': 2.0, \
                   'cupoz': 8.0, 'ozlb': 0.0625, 'lboz': 16.0}
    """The list of fields that need to be updated"""
    ing_list= [float(calories), float(protein), float(fat), float(carbohydrates)\
               , float(sodium), float(sugar), float(sat_fat), float(cholesterol)]
   
    convert_wt= float(convert_wt)
    convert_num = float(convert_num)
    converted_ing= []
    
    """If the units are the same, you don't need to convert units before converting the ingredient"""
    if unit == convert_unit:
   
        convert_wt = (convert_wt/convert_num) * amount
        convert_new = convert_wt / 100
       
        for i in ing_list:
            i = i * convert_new
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing
    """If the unit given by the user is different from the unit in the database then you need to convert
       units before you can convert the ingredients values"""
    if unit != convert_unit:
        val = unit + convert_unit
        amount = amount * convert_val[val]

        convert_wt = (convert_wt/convert_num) * amount
        convert_new = convert_wt / 100
           
        for i in ing_list:
            i = i * convert_new
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

'''The following functions write recipe information to two separate databases,
recipe.sqlite and ingredients.sqlite.'''

"""Adds recipe title and generates recipe_id"""
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

"""Grabs recipe_id to be used as key for ingredients"""
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

"""Writes ingredients to ingredients.sqlite. Also adds recipe_id so ingredients can
#be retrieved"""
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
