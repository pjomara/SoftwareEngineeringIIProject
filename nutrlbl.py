#!/usr/bin/env python 

#Code referenced from http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python

class line:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

serv_size= 13
cal= 250
fat= 10
sat= 3
tran= 0
chol= 0
sod=123
carb=22
sug=10
prot=4

print "\n"
print "\n"
print "___________________________________"
print line.BOLD + "Nutrition Facts" + line.END
print "Serving Size ", serv_size, "g"
print line.UNDERLINE + "___________________________________" + line.END
print line.UNDERLINE + "Amount Per Serving                 " + line.END
print line.UNDERLINE + "Calories ", cal, "                     " + line.END
print line.UNDERLINE + "                     % Daily Value*" + line.END
print line.UNDERLINE + "Total Fat ", fat, "g                    " + line.END
print line.UNDERLINE + "   Saturated Fat ", sat, "g              " + line.END
print line.UNDERLINE + "   Trans Fat ", tran, "g                  " + line.END
print line.UNDERLINE + "Cholesterol ", chol, "mg                  " + line.END
print line.UNDERLINE + "Sodium ", sod, "mg                     " + line.END
print line.UNDERLINE + "Total Carbohydrate ", carb, "g           " + line.END
print line.UNDERLINE + "   Sugars ", sug, "g                    " + line.END
print line.UNDERLINE + "Protein ", prot, "g                       " + line.END
print line.UNDERLINE + "___________________________________" + line.END
print "*Percent Daily Values are based on"
print " a 2,000 calorie diet. Your daily"
print " values may be higher or lower "
print line.UNDERLINE + " depending on your calorie needs.  " + line.END
print "\n"
