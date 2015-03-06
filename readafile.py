import numpy as np


def readafile(filename):
	return np.genfromtxt(filename,usecols=(1,2,3),unpack=True)

x,y,z=readafile("trajectory0.txt")
print x
print y
print z
