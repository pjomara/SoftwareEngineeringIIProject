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
        if ingredient:
            ingredients =[]
            description, calories, protein, fat, carbohydrates, sodium,\
                sugar, sat_fat, cholesterol, convert_wt, convert_num, convert_unit=\
                nutr_grabber(ingredient)
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
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, servSize)
    num_ingr = len(recipe)-1
    recipe.append(num_ingr)

'''Submits the ingredient name and returns the nutritional information.'''
def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDAData.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, FA_Sat_g,Cholestrl_g, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg, Gm_unit, num, unit from USDADataProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protein= row[2]
                fat= row[3]
                carbohydrates= row[4]
                sodium= row[10]
                sugar= row[6]
                Sat_fat= row[8]
                Cholesterol= row[9]
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
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar, servSize):

$servSize=servSize

    recipe= open("label.html", "a")
    print ("""
<html>
<head>
<!--Code referenced from the following-->

<!--http://stackoverflow.com/questions/4513388/how-to-underline-blank-space-in-css-->

<!--http://www.ironspider.ca/format_text/fontstyles.htm-->


<title>Nutrition Label</title>
</head>
<body>

<p style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 2px solid black;"></span>

<h3>Nutrition Facts</h3>

<h3>Valeur nutritive</h3>
""", file=recipe)

print ("""<p style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 3px solid black;">Per $servSize servings </span></p>""", file=recipe)

print("""<h6 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;"> Teneur&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;% Daily Value*</span></h6>""", file=recipe)

print("""<h5 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;">Calories """,  tot_calories, """ </h5></span>""", file=recipe)


print("""<h5 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;">Total Fat """, tot_fat, ' g', """ </span></h5>""", file=recipe)

print("""<h5 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;">Sodium """, tot_sodium, 'mg', """</span></h5>""", file=recipe)

print("""<h5 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;">Carbohydrate """, tot_carb, ' g', """</span></h5>""", file=recipe)

print("""<h6 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 1px solid black;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sugar """, tot_sugar, ' g', """</span></h6>""", file=recipe)

print("""<h5 style="width: 300px; display: table;">
<span style="display: table-cell; border-bottom: 3px solid black;">Protein """,  tot_protein, ' g', """</span></h5>""", file=recipe)

print("""<h5>*Pourcentage des valeurs quotidiennes </h5>

<h5 style="width: 300px; display: table;"><span style="display: table-cell; border-bottom: 2px solid black;"> sur un régime de 2,000 calories.</span></h5>
</body></html>""", file=recipe)

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
    tspInCup= 48.0
    tbspInCup= 16.0
    tspInTbsp= 3.0
    flozInCup= 8.0
    flozInTbsp= 0.5
    ozInLb= 16.0
    
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

    if unit == "cup" and convert_unit == "tbsp":
    
        convert_wt = (convert_wt/convert_num) * (amount * tbspInCup)
        convert_val = convert_wt / 100
        
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing
        
    if unit == "cup" and convert_unit == "tsp":
    
        convert_wt = (convert_wt/convert_num) * (amount * tspInCup)
        convert_val = convert_wt / 100
        
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "tsp" and convert_unit == "cup":

        convert_wt = (convert_wt/convert_num) * (amount / tspInCup)
        convert_val = convert_wt / 100
        
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "tsp" and convert_unit == "tbsp":

        convert_wt = (convert_wt/convert_num) * (amount / tspInTbsp)
        convert_val = convert_wt / 100

        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i,2))
        return converted_ing

    if unit == "tbsp" and convert_unit == "cup":
    
        convert_wt = (convert_wt/convert_num) * (amount / tbspInCup)
        convert_val = convert_wt / 100    
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "tbsp" and convert_unit == "tsp":
    
        convert_wt = (convert_wt/convert_num) * (amount * tspInTbsp)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "oz" and convert_unit == "tbsp":
    
        convert_wt = (convert_wt/convert_num) * (amount * flozInTbsp)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "oz" and convert_unit == "cup":
    
        convert_wt = (convert_wt/convert_num) * (amount / flozInCup)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "tbsp" and convert_unit == "oz":
    
        convert_wt = (convert_wt/convert_num) * (amount / flozInTbsp)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i,2))
        return converted_ing

    if unit == "cup" and convert_unit == "oz":
    
        convert_wt = (convert_wt/convert_num) * (amount * flozInCup)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "oz" and convert_unit == "lb":
    
        convert_wt = (convert_wt/convert_num) * (amount / ozInLb)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
            i = i / float(servSize)
            converted_ing.append(round(i, 2))
        return converted_ing

    if unit == "lb" and convert_unit == "oz":
    
        convert_wt = (convert_wt/convert_num) * (amount * ozInLb)
        convert_val = convert_wt / 100
    
        for i in ing_list:
            i = i * convert_val
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
            c.execute("INSERT INTO ingredient (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugarsat_fat, cholesterol)\
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar, sat_fat, cholesterol))
            conn.commit()
        finally:
            c.close()
    finally:
        conn.close()

    
main()
