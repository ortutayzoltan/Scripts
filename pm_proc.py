#!/usr/bin/python

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="Parse PM file named FILE", metavar="FILE")
parser.add_option("-d", "--dir", dest="directory", help="Parse all PM files in DIRECTORY", metavar="DIRECTORY")
(options, args) = parser.parse_args()
namespace = { "measCollec" : "http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec"}

def buildMeasTypesDict(file_name):
	resultDict = {}
	tree = ET.parse(file_name)
	root = tree.getroot()
	mtd = {}
	for measInfo in root[1]:
		#Build dictionary of meas types
		tmp_measTypesDict = {}
		measTypes = measInfo.findall('measCollec:measType',namespace)
		for measType in measTypes:
			tmp_measTypesDict[measType.get('p')] = measType.text
		mtd[measInfo.get('measInfoId')] = tmp_measTypesDict
	return mtd

#def gatherInfo(file_name,measTypesDict,measInfoId,measName):
#	resultDict = {}
#	tree = ET.parse(file_name)
#	root = tree.getroot()
#	for measInfo in root[1]:
#		if measInfo.get('measInfoId') != measInfoId:
#			continue
#		#resultDict['endTime'] = measInfo.find('measCollec:granPeriod',namespace).get('endTime')
#		resultDict['endTime'] = measInfo[1].get('endTime')
#		#Parsing measValue-s
#		resultDict['measures']=[]
#		measValues = measInfo.findall('measCollec:measValue',namespace)
#		for measValue in measValues:
#			measObj =  measValue.get('measObjLdn')
#			rs = measValue.findall('measCollec:r',namespace)
#			for r in rs:
#				name= measTypesDict[measInfoId][r.get('p')]
#				if name != measName:
#					continue
#				value =  r.text
#				resultDict['measures'].append({'object':measObj,'name':name,'value':value})
#	return resultDict

def gatherInfo(file_name,measTypesDict,measInfoId,measName):
	resultDict = {}
	tree = ET.parse(file_name)
	root = tree.getroot()
	measInfo = root[1].find("measCollec:measInfo[@measInfoId='" + measInfoId +"']",namespace)
	resultDict['endTime'] = measInfo[1].get('endTime')
	#Parsing measValue-s
	resultDict['measures']=[]
	myP = measTypesDict[measInfoId].keys()[measTypesDict[measInfoId].values().index(measName)]
	measValues = measInfo.findall('measCollec:measValue',namespace)
	for measValue in measValues:
		measObj =  measValue.get('measObjLdn')
		r = measValue.find("measCollec:r[@p='"+myP +"']",namespace)
		value =  r.text
		resultDict['measures'].append({'object':measObj,'name':measName,'value':value})
	return resultDict

def formatInfo(infoDict):
	#json_object = json.loads(infoDict)
	#print json.dumps(infoDict, indent=2)
	et = infoDict['endTime']
        print 'Timestamp;Object;Value'
	for m in infoDict['measures']:
		print et+';'+ m['object']+';'+ m['value']

if (options.filename is not None):
	info = gatherInfo(options.filename,buildMeasTypesDict(options.filename),"SBG_Payload_ApplStats_CounterGroup",'sbgApplCPUUsageMax')
	formatInfo(info)
	#print(json.dumps(buildMeasTypesDict(options.filename),indent=2))
	sys.exit()
	
if (options.directory is not None):
	files = os.listdir(options.directory)
	for name in [f for f in files if re.match(r'^A.*\.xml$',f)]:
		info = gatherInfo(options.directory + name)
		formatInfo(info)

