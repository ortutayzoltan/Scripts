#!/usr/bin/python3
import os
import re
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
from openpyxl import Workbook


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="Parse PM file named FILE", metavar="FILE")
parser.add_option("-i", "--measInfoId", dest="measInfoId", help="measInfoId", metavar="measInfoId")
parser.add_option("-p", "--p", dest="p", help="p", metavar="p")
(options, args) = parser.parse_args()
namespace = '{http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec}'



def create_xpath_string_for_measurements(ns,measInfoId,p):
	return './/' + ns + 'measInfo[@measInfoId="' + measInfoId + '"]/' + ns + 'measValue/' + ns + 'r[@p="' + p +'"]'
	
def create_xpath_string_for_measValues(ns,measInfoId):
	return './/' + ns + 'measInfo[@measInfoId="' + measInfoId + '"]/' + ns + 'measValue'
	
def create_xpath_string_for_measTypes(ns,measInfoId):
	return './/' + ns + 'measInfo[@measInfoId="' + measInfoId + '"]/' + ns + 'measType'

def create_xpath_string_for_granPeriod(ns,measInfoId):
	return './/' + ns + 'measInfo[@measInfoId="' + measInfoId + '"]/'  + ns + 'granPeriod'

def set_header(mysheet,header,isFirst):
	if isFirst:
		mysheet.append(['Time'] + header)
		return False
	else:
		return False
		
		
def convert_to_float(string):
	try:
		retval = float(string)
	except:
		retval = string
	return retval
	
	
isFirst = True

wb = Workbook()
sheet = wb.get_sheet_by_name('Sheet')
sheet.title = options.measInfoId[:30]


files = os.listdir('./')
for name in [f for f in files if re.match(r'^A.*\.xml$',f)]:
	tree = ET.parse(name)
	my_measTypes = create_xpath_string_for_measTypes(namespace,options.measInfoId)
	#meaTypeDict ={ measType.get('p') : measType.text for measType in tree.findall(my_measTypes)}
	#not needed for now
	my_xpath_for_measurements = create_xpath_string_for_measurements(namespace,options.measInfoId,options.p)
	my_xpath_for_measValues = create_xpath_string_for_measValues(namespace,options.measInfoId)
	granPeriod = tree.find(create_xpath_string_for_granPeriod(namespace,options.measInfoId))
	isFirst = set_header(sheet,[ (item.get('measObjLdn')) for item  in tree.findall(my_xpath_for_measValues)],isFirst)
	sheet.append( [ granPeriod .get('endTime') ] + [ convert_to_float(item.text) for item  in tree.findall(my_xpath_for_measurements)] )



wb.save(filename = options.measInfoId + '_' + options.p + '.xlsx')
	