import xml.etree.ElementTree as ET
import pudb

def dzi2json(dzifilepath):
	jsondict = {}
	
	tree = ET.parse(dzifilepath)
	xmlroot = tree.getroot()
	if xmlroot.tag == '{http://schemas.microsoft.com/deepzoom/2008}Image':
		jsondict = xmlroot.attrib
		for child in xmlroot:
			if child.tag == '{http://schemas.microsoft.com/deepzoom/2008}Size':
				jsondict['Size'] = child.attrib
				
	
	return jsondict
