Files included/ needed to run app:

nutr_app.py- main file
USDAData.db- sqlite database containing ingredients and nutritional (per 110 gms) information
ingredients.sqlite- collects ingredients and nutritional information
recipe.sqlite-contains recipe tile, serving size, and unique identifier

Additional files:
recipe_retrieve.py- extracts recipes, by title, from recipe.sqlite and ingredients.sqlite databases.  Writes recipe ingredients and nutritional information to the screen.

nutrApp.py-  This is the main file of this project.  From the command-line, use is asked for a recipe title and serving size. This is written to recipe.sqlite.  Also, recipe is given a unique id number.  User then asked for ingredients (amount, unit, description).  Ingredient nutritional information (calories, protein, fat, carbohydrates, sodium, and sugar) are queried and returned from USDAData.db file.  Returned information is passed through convert() function.  Here ingredient nutritional information is converted from per 100 gm to the amount and unit given.  This informaiton is passed back, written to recipe_book.txt 


When the program is started, the user is asked to enter a recipe name. Then the program asks the user for the serving size, amount, unit of measurement, and the ingredient. Then the user is asked “More ingredients? (Enter 'yes' or 'no')”. If they enter no, the program is over. If the user enters yes, they are asked again the amount, unit of measurement, and ingredient. After the user is done inputting ingredients, the recipe is saved to a text file "recipe_book.txt". In the text file, the nutritional information for the recipe they created is displayed similarly to a nutritional label on everyday food products. The nutritional information includes the amount of calories, total fat (including saturated fat), cholesterol, sodium, carbohydrates, sugars, protein, and the daily value percentage of each.
