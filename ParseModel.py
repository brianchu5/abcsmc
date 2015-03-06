from lxml.etree import ElementTree as ET



def modifyModel(parameter,value):
	mydoc = ET(file='dimer_decay.xml')
	if parameter=="c1":
		mydoc.findall('./ParametersList/Parameter/Expression')[0].text=value
	elif parameter == "c2":
		mydoc.findall('./ParametersList/Parameter/Expression')[1].text=value
	elif parameter == "c3":
		mydoc.findall('./ParametersList/Parameter/Expression')[2].text=value
	mydoc.write("dimer_decay.xml")			


modifyModel("c1","1000")




