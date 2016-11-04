'''Il s'agit d'un programme en ligne de commande qui demande la quantité, l'unité et le nom de l'ingrédient.
Compile chaque ingrédient dans un fichier .txt nommé recipe_book.txt.
Interroge une base de données d'ingrédients, tire des informations nutritionnelles. Pour chaque ingrédient.
Imprime des informations nutritionnelles cumulatives. À recipe_book.txt. Cette version met également
Ingrédients dans une liste. La liste contient le titre de la recette, la liste
Ingrédient contenant des informations nutritionnelles et le nombre d'ingrédients
la recette'''

import sqlite3

def main():
    recipe =[]
    title= input("Entrez le titre de la recette: ")
    servSize= eval(input("Entrez la taille de la portion: "))
    recipe_write_dbase(title, servSize)
    recipe.append(title)
    recipe.append(servSize)
    title_write(title, servSize)
    more= 'oui'
    tot_calories= float(0)
    tot_protein= float(0)
    tot_fat= float(0)
    tot_carb= float(0)
    tot_sodium= float(0)
    tot_sugar= float(0)
    while more == 'oui':
        amount = eval(input("Entrer le montant: "))
        unit = input("Entrer dans l'unité(ex. - coupe, cuillère à café); ")
        ingredient = input("Entrez l'ingrédient: ")
        if ingredient:
            ingredients =[]
            ####
            description, calories, protein, fat, carbohydrates, sodium,\
                sugar, convert_wt, convert_num, convert_unit=\
                nutr_grabber(ingredient)
            converted_ingr= convert(amount, servSize, unit, calories, protein, fat,\
                                    carbohydrates, sodium, sugar, convert_wt,\
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
            more = input("Plus d'ingrédients? (Entrer 'oui' or 'non'):")
    nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar)
    num_ingr = len(recipe)-1
    recipe.append(num_ingr)

'''Soumet le nom de l'ingrédient et renvoie l'information nutritionnelle.'''
def nutr_grabber(ingredient):
    conn= sqlite3.connect('USDAData.db')
    try:
        c = conn.cursor()
        try:
            c.execute("select Shrt_Desc, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g, Calcium_mg, Iron_mg, Magnesium_mg, Sodium_mg, Gm_unit, num, unit from USDADataProto where Shrt_Desc like ?", ('%'+ingredient+'%',))

            row= c.fetchone()
            if row:
                description = row[0]
                calories= row[1]
                protéine= row[2]
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
                protéine= None
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

    return description, calories, protéine, fat, carbohydrates, sodium, sugar, convert_wt, convert_num, convert_unit

#Imprime le titre de la recette sur recipe_book.txt
def title_write(title, servSize):
    recipe= open("recipe_book.txt", "a")
    print (title, file=recipe)
    print ("Serves: ", servSize, file=recipe)
    recipe.close()

#Imprime le montant, l'unité et l'ingrédient à recipe_book.txt
def recipe_write(amount, unit, description):
    recipe= open("recipe_book.txt", "a")
    print (amount,' ', unit,' ',description, file=recipe)
    recipe.close()

#Imprime des informations nutritionnelles sur recipe_book.txt
def nutr_write(tot_calories, tot_protein, tot_fat, tot_carb, tot_sodium, tot_sugar):
    recipe= open("recipe_book.txt", "a")
    print ("Nutritional information", file=recipe)
    print ("calories: ",round(tot_calories,0), file=recipe)
    print ("Protein: ", round(tot_protein, 2),' gm', file=recipe)
    print ("Fat: ", round(tot_fat, 2), ' gm', file=recipe)
    print ("Carbohydrates: ", round(tot_carb, 2),' gm', file=recipe)
    print ("Sodium: ", round(tot_sodium, 2),' mg', file=recipe)
    print ("Sugar: ", round(tot_sugar, 2),' gm', file=recipe)
    recipe.close()
    
'''Cette fonction convertit les valeurs nutritionnelles de chaque nutriment dans chaque
Ingrédient par 100 gm pour ce qui est jamais demandé dans la recette.
Par exemple, couvre l'information nutritionnelle pour 100 grammes de farine à la nutrition
Information pour 2 sups farine. Si nécessaire, les unités (tasse, tsp, tbsp) sont convertis en
Quelle que soit l'unité la plus commune pour cet ingrédient. Par exemple, une recette donne
La quantité de farine en tbsp, ce sera converti en tasses (le plus couramment
Utilisé pour mesurer la farine).'''
def convert(amount, servSize, unit, calories, protein, fat, carbohydrates, sodium, sugar\
            , convert_wt, convert_num, convert_unit):
    #Convertir des facteurs
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

'''Les fonctions suivantes écrivent des informations de recette à deux bases de données distinctes,
Recette.sqlite et ingredients.sqlite.'''

#Ajoute le titre de la recette et génère recipe_id.
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

#Attrape recepe_id à utiliser comme clé pour les ingrédients.
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

#Écrit les ingrédients dans les ingrédients.sqlite. Ajoute également recipe_id afin que les ingrédients puissent
#être récupérés.
def ingredient_write_dbase(recipe_id, amount, unit, ingredient, converted_ingr):
    calories, protein, fat, carbohydrates, sodium, sugar= converted_ingr
    conn= sqlite3.connect("ingredients.sqlite")
    try:
        c=conn.cursor()
        try:
            c.execute("INSERT INTO ingredient (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar)\
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recipe_id, amount, unit, ingredient, calories, protein, fat, carbohydrates, sodium, sugar,))
            conn.commit()
        finally:
            c.close()
    finally:
        conn.close()

    
main()

