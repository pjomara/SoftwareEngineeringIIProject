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
    recipe_write_dbase(title)
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
    sat_fat= float(0)
    tot_chol= float(0)
    
    while more == 'yes':
        amount = eval(input("Enter amount: "))
        unit = input("Enter the unit(I.E.- cup, tsp); ")
        ingredient = input("Enter the ingredient: ")
        if ingredient:
            ingredients =[]
            description, calories, protein, fat, carbohydrates, sodium,\
                sugar, satfat, cholesterol, convert_wt, convert_num, convert_unit=\
                nutr_grabber(ingredient)
            converted_ingr= convert(amount, servSize, unit, calories, protein, fat,\
                                    carbohydrates, sodium, sugar, satfat, cholesterol,\
                                    convert_wt, convert_num, convert_unit, )
            recipe_id= id_grabber(title)
            ingredient_write_dbase(recipe_id, amount, unit, ingredient, converted_ingr)
            ingredients = [amount, unit, ingredient, converted_ingr]            
            recipe.append(ingredients)
            recipe_write(amount, unit, description)
            tot_calories= tot_calories + converted_ingr[0]
            tot_protein = tot_protein + converted_ingr[1]
            tot_fat = tot_fat + converted_ingr[2]
            tot_carb = tot_carb + converted_ingr[3]
            tot_sodium= tot_sodium + converted_ingr[4]/1000
            tot_sugar= tot_sugar + converted_ingr[5]
            sat_fat= sat_fat + converted_ingr[6]
            tot_chol= tot_chol + converted_ing[7]/1000
            
            more = input("More ingredients? (Enter 'yes' or 'no'):")
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, sat_fat, tot_chol)
    num_ingr = len(recipe)-1
    recipe.append(num_ingr)

'''Submits the ingredient name and returns the nutritional information.'''
def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDAData.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, FA_Sat_g, Cholestrl_mg, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg, Gm_unit, num, unit from USDADataProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protein= row[2]
                fat= row[3]
                carbohydrates= row[4]
                sodium= row[10]
                sugar= row[6]
                satfat= row[]
                cholesterol= row[]
                convert_wt= row[11]
                convert_num= row[12]
                convert_unit= row[13]
                
            else:
                description = None
                calories= None
                protein= None
                fat= None
                carbohydrates= None
                sodium= None
                sugar= None
                satfat= None
                cholesterol = None
                convert_wt= None
                convert_num= None
                convert_unit= None

        finally:
            c.close()

    finally:
        conn.close()

    return description, calories, protein, fat, carbohydrates, sodium, sugar, satfat, cholesterol, convert_wt, convert_num, convert_unit

#prints title of recipe to recipe_book.txt
def title_write(title, servSize):
    recipe= open("recipe_book.txt", "a")
    print (title, file=recipe)
    print ("Service size: ", servSize, file=recipe)
    recipe.close()

#prints amount, unit, and ingredient to recipe_book.txt
def recipe_write(amount, unit, description):
    recipe= open("recipe_book.txt", "a")
    print (amount,' ', unit,' ',description, file=recipe)
    recipe.close()

#prints nutritional information to recipe_book.txt
def nutr_write(serving_size, tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, sat_fat, tot_chol):
    
    #Code referenced from http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
    class line:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    tot_ft_dv =65.0
    tot_chol_dv =300.0
    tot_sod_dv =2400.0
    tot_carb_dv =300.0
    tot_prot_dv =50.0

    ft_dv= (tot_fat/tot_ft_dv)*100
    #chol_dv= (tot_chol/tot_chol_dv)*100
    sod_dv= (tot_sod/tot_sod_dv)*100
    carb_dv= (tot_carb/tot_carb_dv)*100
    prot_dv= (tot_prot/tot_prot_dv)*100
    
    recipe= open("recipe_book.txt", "a")
    print "_______________________________"
    print line.BOLD + "Nutrition Facts" + line.END, file=recipe
    print "Serving Size ", int(serv_size), "g", file=recipe
    print line.UNDERLINE + "_______________________________" + line.END, file=recipe
    print line.UNDERLINE + "Amount Per Serving             " + line.END, file=recipe
    print line.UNDERLINE + "Calories ", int(tot_calories), "                 " + line.END, file=recipe
    print line.UNDERLINE + "                 % Daily Value*" + line.END, file=recipe
    print line.UNDERLINE + "Total Fat ", int(tot_fat), "g           ", int(ft_dv),"%" + line.END, file=recipe
    #print line.UNDERLINE + "   Saturated Fat ", int(sat), "g          " + line.END, file=recipe
    #print line.UNDERLINE + "   Trans Fat ", int(tran), "g              " + line.END, file=recipe
    #print line.UNDERLINE + "Cholesterol ", int(chol), "mg       ", int(chol_dv), "%" + line.END, file=recipe
    print line.UNDERLINE + "Sodium ", int(tot_sod), "mg             ", int(sod_dv), "%" + line.END, file=recipe
    print line.UNDERLINE + "Total Carbohydrate ", int(tot_carb), "g   ", int(carb_dv), "%" + line.END, file=recipe
    #print line.UNDERLINE + "   Sugars ", int(sug), "g                " + line.END, file=recipe
    print line.UNDERLINE + "Protein ", int(tot_prot), "g               ", int(prot_dv), "%" + line.END, file=recipe
    print line.UNDERLINE + "_______________________________" + line.END, file=recipe
    print "*Percent Daily Values are based", file=recipe
    print line.UNDERLINE + " on a 2,000 calorie diet.      " + line.END, file=recipe
    print "/n"
    recipe.close()
    
'''This function converts the nutritional values for each nutrient in each
ingredient from per 100 gm to what ever is called for in the recipe.
For example, coverts nutritional information for 100 gms of flour to nutritional
information for 2 sups flour.  If needed, units (cup, tsp, tbsp) are converted into
whatever is the most common unit for that ingredient.  For example, a recipe gives
the flour amount in tbsp, this will be converted into cups (the most commonly
used unit to measure flour).'''
def convert(amount, servSize, unit, calories, protein, fat, carbohydrates, sodium, sugar, satfat, cholesterol\
            , convert_wt, convert_num, convert_unit):
    #Convert factors
    convert_val = {'cuptsp': 48.0, 'tspcup': 1/48.0, 'cuptbsp': 16.0, 'tsptbsp': 1/3.0, \
                   'tbsptsp': 3.0, 'ozcup': 1/8.0, 'oztbsp': 0.5, 'tbspoz': 2.0, \
                   'cupoz': 8.0, 'ozlb': 1/16.0, 'lboz': 16.0}
    
    ing_list= [float(calories), float(protein), float(fat), float(carbohydrates)\
               , float(sodium), float(sugar), float(satfat), float(cholesterol) ]
    
    convert_val= float
    convert_wt= float(convert_wt)
    convert_num = float(convert_num)
    converted_ing= []
    
    if unit != convert_unit:
        val = unit + convert_unit
	    amount = amount * convert_val[val]

    convert_wt = (convert_wt/convert_num) * amount
    convert_val = convert_wt / 100
        
    for i in ing_list:
        i = i * convert_val
        i = i / float(servSize)
        converted_ing.append(round(i, 2))
    return converted_ing
    
    
'''The following functions write recipe information to two separate databases,
recipe.sqlite and ingredients.sqlite.'''

#adds recipe title and generates recipe_id.
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
    calories, protein, fat, carbohydrates, sodium, sugar, satfat, cholesterol= converted_ingr
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c=conn.cursor()
        try:
            c.execute("INSERT INTO ingredient (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar, satfat, cholesterol)\
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar, satfat, cholesterol))
            conn.commit()
        finally:
            c.close()
    finally:
        conn.close()

    
main()
