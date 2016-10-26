#!/usr/bin/env python 

#Code referenced from http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python

class line:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

serv_size= 13
cal= 250
fat= 10.0
sat= 3.0
tran= 7.0
chol= 100.0
sod=123.0
carb=22.0
sug=10.0
prot=4.0
tot_ft_dv =65.0
tot_chol_dv =300.0
tot_sod_dv =2400.0
tot_carb_dv =300.0
tot_prot_dv =50.0

ft_dv= (fat/tot_ft_dv)*100
chol_dv= (chol/tot_chol_dv)*100
sod_dv= (sod/tot_sod_dv)*100
carb_dv= (carb/tot_carb_dv)*100
prot_dv= (prot/tot_prot_dv)*100

print "\n"
print "\n"
print "___________________________________"
print line.BOLD + "Nutrition Facts" + line.END
print "Serving Size ", serv_size, "g"
print line.UNDERLINE + "___________________________________" + line.END
print "Amount Per Serving"
print "___________________________________"
print "Calories ", cal
print "                     % Daily Value*"
print "___________________________________"
print "Total Fat ", fat, "g           ", round(ft_dv),"%"
print "___________________________________"
print "   Saturated Fat ", sat, "g            "
print "___________________________________"
print "   Trans Fat ", tran, "g                "
print "___________________________________"
print "Cholesterol ", chol, "mg       ", round(chol_dv), "%"
print "___________________________________"
print "Sodium ", sod, "mg             ", round(sod_dv), "%"
print "___________________________________"
print "Total Carbohydrate ", carb, "g   ", round(carb_dv), "%"
print "___________________________________"
print "   Sugars ", sug, "g                  "
print "___________________________________"
print "Protein ", prot, "g               ", round(prot_dv), "%"
print line.UNDERLINE + "___________________________________" + line.END
print "*Percent Daily Values are based on"
print line.UNDERLINE + " a 2,000 calorie diet.             " + line.END
print "\n"
