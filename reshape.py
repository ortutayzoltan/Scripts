#!/usr/bin/python3

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="Parse PM file named FILE", metavar="FILE")
(options, args) = parser.parse_args()
resdict = {}

if (options.filename is not None):
	filename = options.filename
else:
	filename = 'result.csv'
	
	
obj_list = ['Timestamp']

with open(filename) as file:
	for line in file.readlines():
		(date,obj,value) = line.rstrip('\n').split(';')
		if date == 'Timestamp':
			continue
		if obj not in obj_list:
			obj_list.append(obj)
		if date in resdict :
			resdict[date][obj]=value
		else:
			resdict[date]={obj:value}
print(';'.join(obj_list))
for (k,v) in resdict.items():
	print(k+';'+';'.join([val for (pl,val) in sorted(v.items())]))
	
