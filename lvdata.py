import numpy as np 
import os
import subprocess
from lxml.etree import ElementTree as ET

class realdata:
    def __init__(self):
        self.s1data = []
        self.s2data = []
	self.s3data = []
        self.c1 = 1.0
        self.c2 = 0.002
        self.c3 = 0.5
        self.duration = "20"
        self.s1trial = [np.zeros(3) for i in range(20)]
        self.s2trial = [np.zeros(3) for i in range(20)]
	self.s3trial = [np.zeros(3) for i in range(20)]
        self.runs = 3
	self.smod = "./runF.sh"
	self.model = "dimer_decay.xml"
        

    def gendata(self):
	modifyModel("c1",str(self.c1))
	modifyModel("c2",str(self.c2))
	modifyModel("c3",str(self.c3))
	ind1 = 0
        for i in np.arange(1,21,1):
	  ind2 = 0
	  for j in range(self.runs):
		subprocess.call([self.smod,self.model,self.duration,"1",self.duration])
            	data = readafile("trajectory0.txt")
		data = data.transpose()
		data =  data[data[:,0]==i]
		print data
		#print data[:]
		print i
		#print data_at_time_i[:,1]
		print data[0][1]
                self.s1trial[ind1][ind2]=data[0][1]
                self.s2trial[ind1][ind2]=data[0][2]
		self.s3trial[ind1][ind2]=data[0][3]
                ind2+=1
	  ind1+=1
	self.computeTimeAverages();
        
            


    def computeTimeAverages(self):
        for index in range(9):
            self.s1data.append(self.meanTrialS1(index))
            self.s2data.append(self.meanTrialS2(index))
	    self.s3data.append(self.meanTrialS3(index))
            


    def meanTrialS3(self,index):
        return np.mean(self.s3trial[index])

    def meanTrialS2(self,index):
        return np.mean(self.s2trial[index])
    def meanTrialS1(self,index):
        return np.mean(self.s1trial[index])


def modifyModel(parameter,value):
        mydoc = ET(file='dimer_decay.xml')
        if parameter=="c1":
                mydoc.findall('./ParametersList/Parameter/Expression')[0].text=value
        elif parameter == "c2":
                mydoc.findall('./ParametersList/Parameter/Expression')[1].text=value
        elif parameter == "c3":
                mydoc.findall('./ParametersList/Parameter/Expression')[2].text=value
        mydoc.write("dimer_decay.xml")



def readafile(filename):
        return np.genfromtxt(filename,usecols=(0,1,2,3),unpack=True,dtype=(int))

def main():
  rd = realdata() 
  rd.gendata() 
  print rd.s1data,rd.s2data,rd.s3data

main()

