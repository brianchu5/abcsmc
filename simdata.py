import numpy as np 
import os
import subprocess
from lxml.etree import ElementTree as ET
import random

class DataManager:
    def __init__(self):
        self.kf = 7.5
        self.kb = 0.75
        self.mu = 100
	self.sigma = 20
        self.duration = "10"
        self.s1trial = [[] for i in range(4)]
        self.runs = 3
	self.smod = "./runF.sh"
	self.model = "bd_stochkit.xml"
    
    def samplenormal(self,s):
	arr = np.zeros(len(s))
	ind = 0
	for i in s:
        	arr[ind] = random.normalvariate(100*i,20*i)
        	ind+=1

	return arr

    def trialnormal(self,s,mu,sig):
	arr = np.zeros(len(s))
        ind = 0
        for i in s:
                arr[ind] = random.normalvariate(mu*i,sig*i)
                ind+=1

        return arr
 

    def gendata(self):
	modifyModel("kf",str(self.kf))
	modifyModel("kb",str(self.kb))
	subprocess.call([self.smod,self.model,self.duration,"80000","20"])	
	s1 = readafile("time1.txt")
	s1half = readafile("time0.5.txt")
	s2 = readafile("time2.txt")
	s10 = readafile("time10.txt")
	self.s1trial[0] = self.samplenormal(s1)
	self.s1trial[1] = self.samplenormal(s1half)
	self.s1trial[2] = self.samplenormal(s2)
	self.s1trial[3] = self.samplenormal(s10)


    def trialdata(self,parameters,trials):
	kf = parameters[0]
	kb = parameters[1]
	mu = parameters[2]
	sig = parameters[3]
	modifyModel("kf",str(kf))
        modifyModel("kb",str(kb))
	subprocess.call([self.smod,self.model,self.duration,str(trials),"20"])

	s1 = readafile("time1.txt")
        s1half = readafile("time0.5.txt")
        s2 = readafile("time2.txt")
        s10 = readafile("time10.txt")
	

	self.s1trial[0]=self.trialnormal(s1,mu,sig)
	self.s1trial[1]=self.trialnormal(s1half,mu,sig)
	self.s1trial[2]=self.trialnormal(s2,mu,sig)
	self.s1trial[3]=self.trialnormal(s10,mu,sig)	
	







	
		
	
def readafile(filename):
        return np.genfromtxt(filename,usecols=(1),unpack=True,dtype=(int))	

def modifyModel(parameter,value):
        mydoc = ET(file='bd_stochkit.xml')
        if parameter=="kb":
                mydoc.findall('./ParametersList/Parameter/Expression')[0].text=value
        elif parameter == "kf":
                mydoc.findall('./ParametersList/Parameter/Expression')[1].text=value
        mydoc.write("bd_stochkit.xml")


def generateRealData():
	dm  = DataManager()
	dm.gendata()
	return dm.s1trial



def main():

   dm = DataManager()

   dm.gendata()




	


