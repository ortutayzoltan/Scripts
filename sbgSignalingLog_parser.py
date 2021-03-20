#!/usr/bin/python3
import os
import re
import sys
from optparse import OptionParser
from openpyxl import Workbook

parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory",default = '.' ,help="dir", metavar="FILE")
parser.add_option("-f", "--file", dest="filename",default=[],action='append',help="file", metavar="FILE")
(options, args) = parser.parse_args()
if options.filename == []:
	sbgSignalingLogs = [f for f in os.listdir(options.directory) if re.match(r'^sbgSignalingLog.*\.log$',f)]
else:
	sbgSignalingLogs = options.filename

def transform(line):
	myMatch = re.match('^(.*) PayloadMatedPair=(\d+) (.*) +', line)
	if myMatch is not None:
		retval = [ myMatch.group(1) , myMatch.group(2) ] + myMatch.group(3).split(',')
		retval[-1] = retval[-1].strip()
		while len(retval) < 10:
			retval.append('')
		return retval
	else:
		return []

lines = []
wb = Workbook()
sheet = wb.get_sheet_by_name('Sheet')
sheet.append(['Timestamp','PMP Id' ,'SIP method' ,'Response code' ,'Source IP' ,'Destination IP' ,'Network Id' ,'Call ID' ,'Caller uri','Callee uri'])
for fileName in sbgSignalingLogs:
	with open(fileName) as sbgSignalingLog:
		line = sbgSignalingLog.readline()
		try:
			sheet.append(transform(line))
		except:
			print(transform(line))
		while line:
			try:
				line = sbgSignalingLog.readline()
			except:
				line = ''
			try:
				sheet.append(transform(line))
			except:
				print(transform(line))
#1048576
sheet.auto_filter.ref = "A1:J1048576"
wb.save(filename = 'sbgSignalingLog.xlsx')
