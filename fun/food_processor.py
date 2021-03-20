#!/usr/bin/python3
import csv
import re , os
import matplotlib.pyplot as plt


daily_data = {}

with open('food.csv') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		if row[0] == 'date':
			continue
		date = row[0]
		calories = float(row[7])
		carbs = float(row[8]) * 4
		fats = float(row[12]) * 9
		proteins = float(row[16]) * 4
		if date in daily_data.keys():
			daily_data[date]['calories'] += calories
			daily_data[date]['carbs'] += carbs
			daily_data[date]['fats'] += fats
			daily_data[date]['proteins'] += proteins
			#print(daily_data)
		else:
			daily_data[date] = {'calories' :0 , 'carbs' :0, 'fats':0, 'proteins' : 0}


days = daily_data.keys()
c  = [v['carbs']  for v in daily_data.values()]
f  = [v['fats']  for v in daily_data.values()]
p  = [v['proteins']  for v in daily_data.values()]
#plt.plot(c)
#plt.plot(f)
#plt.plot(p)
#plt.savefig("test.svg", format="svg")
plt.bar(days, c, color='blue')
plt.bar(days, f, bottom = c,color='green')
plt.bar(days, f, bottom = [i+j for i,j in zip(c, f)],color='red')
plt.xticks(range(len(days)), days, rotation='vertical')
plt.show()

