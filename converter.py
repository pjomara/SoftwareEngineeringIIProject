#! /usr/bin/env python3


#def Update(ingredient[], float val):
    
    


val = x #The most common usage number
convert = 0 #The conversion factor
num = x #The amount of a unit input by the user
unit = x #The unit selected by the user
dataunit = x # The most common unit from the database

while ingredient[i] !=0:

    for x in ingredient[x]:
        y = ingredient[x]
        y = y/val
        ingredients.append(y)


        else:
            temp = 0
            
            if unit == tbsp and dataunit == cup:
                val= val/16
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++i

            if unit == tbsp and dataunit == tsp:
                val= val * 3
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++i

            if unit == cup and dataunit == tbsp:
                val= val * 16
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++i

            if unit == cup and dataunit == tsp:
                val= val * 48
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++i
                
            if unit == tsp and dataunit == cup:
                val= val/48
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++i

            if unit == tsp and dataunit == tbsp:
                val= val/3
                temp= val * num
                convert= 100/temp
                    
                Update(convert)
                ++1