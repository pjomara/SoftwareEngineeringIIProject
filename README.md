Files included/ needed to run app:

nutr_app.py- main file
USDAData.db- sqlite database containing ingredients and nutritional (per 110 gms) information
ingredients.sqlite- collects ingredients and nutritional information
recipe.sqlite-contains recipe tile, serving size, and unique identifier

Additional files:
recipe_retrieve.py- extracts recipes, by title, from recipe.sqlite and ingredients.sqlite databases.  Writes recipe ingredients adn nutritional information to the screen.

nutrApp.py-  This is the main file of this project.  From the command-line, use is asked for a recipe title and serving size. This is written to recipe.sqlite.  Also, recipe is given a unique id number.  User then asked for ingredients (amount, unit, description).  Ingredient nutritional information (calories, protein, fat, carbohydrates, sodium, and sugar) are queried adn returned from USDAData.db file.  Returned information is passed through convert() function.  Here ingredient nutritional information is converted from per 100 gm to the amount and unit given.  This informaiton is passed back, written to recipe_bbok.txt 


