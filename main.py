import numpy as np
import simdata
import particle
from particle import particle
from particle import populations
import copy
from scipy import stats


def ks_test(data1, data2,eps):
    """Returns the euclidian distance between two data sets.
    Data sets must have the same dimensions.

    ***** args *****
    
    data1, data2:
            numpy array objects with the same dimensions.

    """

    z,p = stats.ks_2samp(data1,data2)
    return z < eps





def testdistance():
	totalRun = 0
	totalAccepted = 0	
	s1data = simdata.generateRealData() #kf,kb,mu,sigma
	eps_schedule = [0.53,0.318,0.101,0.052]
	simManager = simdata.DataManager()
#	while totalAccepted > 1:
	cp = particle()
	simManager.trialdata(cp.parameters,7)
	ps1,ps2,ps3,ps4 = simManager.s1trial[0],simManager.s1trial[1],simManager.s1trial[2],simManager.s1trial[3]
	print "ps1",ps1 
        print  ks_test(ps1,s1data[0],0.53)		
	print ks_test(ps2,s1data[1],0.53)
	print ks_test(ps3,s1data[2],0.53)
	print ks_test(ps4,s1data[3],0.53)



def abcsmc():
	pop = populations()
	totalRun = 74
        s1data = simdata.generateRealData()
	eps_schedule = [0.772,0.678,0.617,0.568,0.53,0.499,0.473,0.45,0.431,0.414,0.398,0.385,0.373,0.342,0.318,0.298,0.282,0.268,0.249,0.234,0.221,0.21,0.201,0.193,0.186,0.179,0.173,0.168,0.163,0.159,0.155,0.151,0.144,0.139,0.133,0.129,0.125,0.121,0.118,0.114,0.112,0.109,0.106,0.104,0.102,0.1,0.098,0.094,0.09,0.087,0.084,0.081,0.079,0.077,0.075,0.073,0.071,0.065,0.061,0.057,0.054,0.052]
	print len(eps_schedule)
	

	s_c = [3,4,5,6,7,8,9,10,11,12,13,14,15,18,21,24,27,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,275,300,325,350,375,400,425,450,475,500,600,700,800,900,1000]

	print len(s_c)
        simManager = simdata.DataManager()
	for i in range(totalRun):
	   totalAccepted = 0
	   totalruns = 0
           while totalAccepted < 50:
		if i == 0:
	        	cp = particle()
      			simManager.trialdata(cp.parameters,s_c[i])
        		ps1,ps2,ps3,ps4 = simManager.s1trial[0],simManager.s1trial[1],simManager.s1trial[2],simManager.s1trial[3]
        		flag1 = ks_test(ps1,s1data[0],eps_schedule[i])    
        		flag2 = ks_test(ps2,s1data[1],eps_schedule[i])
        		flag3 = ks_test(ps3,s1data[2],eps_schedule[i])
			flag4 = ks_test(ps4,s1data[3],eps_schedule[i])
			if flag1 == True and flag2 ==True and flag3==True and flag4==True:
				pop.addToPopulation(cp)
				totalAccepted+=1
		else:
			cp = copy.copy(pop.pickParticle())
			cp.perturbAll(pop.kernels)
			simManager.trialdata(cp.parameters,s_c[i])
                        ps1,ps2,ps3,ps4 = simManager.s1trial[0],simManager.s1trial[1],simManager.s1trial[2], simManager.s1trial[3]
			flag1 = ks_test(ps1,s1data[0],eps_schedule[i])       
                        flag2 = ks_test(ps2,s1data[1],eps_schedule[i])
                        flag3 = ks_test(ps3,s1data[2],eps_schedule[i])
                        flag4 = ks_test(ps4,s1data[3],eps_schedule[i])
                        if flag1 == True and flag2 ==True and flag3==True and flag4==True:
				pop.assignWeight(cp)
                                totalAccepted+=1
				pop.addToPopulation(cp)
		totalruns+=1


	   print totalruns
	   pop.postprocess()
	   np.savetxt("acceptance."+str(i)+".txt",np.array([totalAccepted/totalruns]))
	   np.savetxt("r1."+str(i)+".txt",np.array(pop.getParameterList(0)))
           np.savetxt("r2."+str(i)+".txt",np.array(pop.getParameterList(1)))
           np.savetxt("r3."+str(i)+".txt",np.array(pop.getParameterList(2)))
	   np.savetxt("r4."+str(i)+".txt",np.array(pop.getParameterList(3)))





	
			


#testdistance()	
abcsmc()			






		
	

