import numpy as np
import random
from scipy import stats


def readafile(filename):
	return np.genfromtxt(filename,usecols=(0,1),unpack=True)

t,s1=readafile("time1.txt")
arr = np.zeros(len(s1))
ind = 0
for i in s1:
	arr[ind] = random.normalvariate(100*i,20*i)
	ind+=1

print stats.ks_2samp(arr,arr)




