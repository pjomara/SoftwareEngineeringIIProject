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
    recipe.append(title)
    recipe.append(servSize)
    title_write(title)
    more= 'yes'
    tot_calories= float(0)
    tot_protein= float(0)
    tot_fat= float(0)
    tot_carb= float(0)
    tot_sodium= float(0)
    tot_sugar= float(0)
    
    tot_fat_dv = 65.0
    chol_dv = 300.0
    sodium_dv = 2400.0
    carb_dv = 300.0
    prot_dv = 50.0
    cal_dv = 2000.0

    while more == 'yes':
        amount = eval(input("Enter amount: "))
        unit = input("Enter the unit(I.E.- cup, tsp); ")
        ingredient = input("Enter the ingredient: ")
        if ingredient:
            ingredients =[]
            description, calories, protein, fat, carbohydrates, sodium,\
                sugar, convert_wt, convert_num, convert_unit=\
                nutr_grabber(ingredient)
            converted_ingr= convert(amount, servSize, unit, calories, protein, fat,\
                                    carbohydrates, sodium, sugar, convert_wt,\
                                    convert_num, convert_unit)
            ingredients = [amount, unit, ingredient, converted_ingr]            
            recipe.append(ingredients)
            recipe_write(amount, unit, description)
            tot_calories= tot_calories + converted_ingr[0]
            tot_protein = tot_protein + converted_ingr[1]
            tot_fat = tot_fat + converted_ingr[2]
            tot_carb = tot_carb + converted_ingr[3]
            tot_sodium= tot_sodium + converted_ingr[4]/1000
            tot_sugar= tot_sugar + converted_ingr[5]
            more = input("More ingredients? (Enter 'yes' or 'no'):")
            
#Calculates the % Daily Value for the serving size            
    for i in ing_list:
        if i = 0
            cal_dv = tot_calories / cal_dv
        if i = 1
            prot_dv = tot_protein / prot_dv 
        if i = 2
            total_fat_dv = tot_fat / total_fat_dv
        if i = 3
            carb_dv = tot_carb / carb_dv
        if i = 4
            sodium_dv = tot_sodium / sodium_dv
        i += 1
        
    nutr_write(cal_dv, prot_dv, total_fat_dv, carb_dv, sodium_dv, tot_sugar)

    #recipe.append(ingredients)
    num_ingr = len(recipe)-1
    recipe.append(num_ingr)
    print (recipe)

def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDADataProto.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg, Gm_unit, num, unit from USDADataProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protein= row[2]
                fat= row[3]
                carbohydrates= row[4]
                sodium= row[10]
                sugar= row[6]
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
                convert_wt= None
                convert_num= None
                convert_unit= None

        finally:
            c.close()

    finally:
        conn.close()

    return description, calories, protein, fat, carbohydrates, sodium, sugar, convert_wt, convert_num, convert_unit

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
    #fixed 9/29
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar):
    recipe= open("recipe_book.txt", "a")
    print ("\n","Nutritional information", file=recipe)
    print ("calories: ",round(tot_calories,0), file=recipe)
    print ("Protein: ", round(tot_protein, 2),' gm', file=recipe)
    print ("Fat: ", round(tot_fat, 2), ' gm', file=recipe)
    print ("Carbohydrates: ", round(tot_carb, 2),' gm', file=recipe)
    print ("Sodium: ", round(tot_sodium, 2),' mg', file=recipe)
    print ("Sugar: ", round(tot_sugar, 2),' gm', file=recipe)
    recipe.close()
    
'''This function converts the nutritional values for each nutrient in each
ingredient from per 100 gm to what ever is called for in the recipe.
For example, coverts nutritional information for 100 gms of flour to nutritional
information for 2 sups flour.  If needed, units (cup, tsp, tbsp) are converted into
whatever is the most common unit for that ingredient.  For example, a recipe gives
the flour amount in tbsp, this will be converted into cups (the most commonly
used unit to measure flour).'''
def convert(amount, servSize, unit, calories, protein, fat, carbohydrates, sodium, sugar\
            , convert_wt, convert_num, convert_unit):
    #Convert factors
    tspInCup= 48.0
    tbspInCup= 16.0
    tspInTbsp= 3.0
    flozInCup= 8.0
    flozInTbsp= 0.5
    ozInLb= 16.0
    
    ing_list= [float(calories), float(protein), float(fat), float(carbohydrates)\
               , float(sodium), float(sugar)]
    
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
    
main()
