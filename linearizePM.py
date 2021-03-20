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

# #		<measInfo measInfoId="SBG_Payload_ApplStats_CounterGroup">
# <job jobId="USERDEF-ISG101CRO.Cont.Y.STATS"/>
# <granPeriod duration="PT900S" endTime="2020-09-01T04:30:00+01:00"/>
# <repPeriod duration="PT900S"/>
# <measType p="1">sbgApplCPUUsage</measType>
# <measType p="2">sbgApplCPUUsageAvg</measType>

def gatherInfo(file_name):
	resultDict = {}
	tree = ET.parse(file_name)
	root = tree.getroot()
	measData = root.find('measCollec:measData',namespace)
	#managedElement = measData.find('measCollec:managedElement',namespace)
	# Node name and SW version
	#resultDict['node'] = managedElement.get('localDn').split('=')[1]
	#resultDict['swVersion'] = managedElement.get('swVersion') 
	measInfos = measData.findall('measCollec:measInfo',namespace)
	for measInfo in measInfos:
		if measInfo.get('measInfoId') != "SBG_Payload_ApplStats_CounterGroup":
			continue
		resultDict['endTime'] = measInfo.find('measCollec:granPeriod',namespace).get('endTime')
		#Build dictionary of meas types
		measTypes = measInfo.findall('measCollec:measType',namespace)
		measTypesDict = {}
		for measType in measTypes:
			measTypesDict[measType.get('p')] = measType.text
		measValues = measInfo.findall('measCollec:measValue',namespace)
		#Parsing measValue-s
		resultDict['measures']=[]
		for measValue in measValues:
			measObj =  measValue.get('measObjLdn')
			rs = measValue.findall('measCollec:r',namespace)
			for r in rs:
				name= measTypesDict[r.get('p')]
				if name != 'sbgApplCPUUsageMax':
					continue
				value =  r.text
				resultDict['measures'].append({'object':measObj,'name':name,'value':value})
	return resultDict

def formatInfo(infoDict):
	#json_object = json.loads(infoDict)
	#print json.dumps(infoDict, indent=2)
	et = infoDict['endTime']
        print 'Timestamp;Object;Value'
	for m in infoDict['measures']:
		print et+';'+ m['object']+';'+ m['value']

if (options.filename is not None):
	info = gatherInfo(options.filename)
	formatInfo(info)
	sys.exit()
	
if (options.directory is not None):
	files = os.listdir(options.directory)
	for name in [f for f in files if re.match(r'^A.*\.xml$',f)]:
		info = gatherInfo(options.directory + name)
		formatInfo(info)

