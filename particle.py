import numpy as np
from operator import attrgetter
from numpy import random as rnd
from copy import deepcopy

class perturbationKernel:
        def __init__(self,lower,upper):
                scale = upper - lower
                self.lower = -scale/2.0
                self.upper = scale/2.0


        def reinitialize(self,lower,upper):
                scale = upper - lower
                self.lower = -scale/2.0
                self.upper = scale/2.0

class populations:
        def __init__(self):
                self.particles =[]
                self.previous_particles = []
                self.kernels = [perturbationKernel(0,0),perturbationKernel(0,0),perturbationKernel(0,0),perturbationKernel(0,0)]
                self.weights = []



	def getParameterList(self,index):
	       return [particle.parameters[index] for particle in self.previous_particles]
	


	def addToPopulation(self,particle):
                self.particles.append(particle)
	def postprocessfromprior(self):
		self.previous_particles = deepcopy(self.particles)

	def postprocess(self):
                self.previous_particles = deepcopy(self.particles)
		self.computeKernel(self.kernels)
		self.weightParticle()
                self.weights = [particle.weight for particle in self.previous_particles]
                self.particles = []


	def computeKernel(self,kernels):
		ind = 0
		for kernel in self.kernels:
                	kernel.reinitialize(self.getMinParameter(ind),self.getMaxParameter(ind)) 
			ind+=1
	



	def pickParticle(self):
                return np.random.choice(self.previous_particles,p=self.weights)



	def weightParticle(self):
                totalweight = 0
		totalweight = sum((i.weight for i in self.previous_particles))
                for particle in self.previous_particles:
                        particle.weight=particle.weight/totalweight

	def assignWeight(self,cparticle):
                num = 1 
                pweights=[]
                for particle in self.previous_particles:
			pweight = particle.weight
			for i in range(4):
                        	scale2 = particle.parameters[i] + self.kernels[i].upper
                        	scale1 = particle.parameters[i] + self.kernels[i].lower
                        	prob = pdensity(scale1,scale2,cparticle.parameters[i])
				pweight = pweight * prob	
                        pweights.append(particle.weight*pweight)

                denom = sum(pweights)
                cparticle.weight = num/denom



	def getMaxParameter(self,index):
                	return max(p.parameters[index] for p in self.previous_particles)

        def getMinParameter(self,index):
                	return min(p.parameters[index] for p in self.previous_particles)





class particle:
        def __init__(self):
                self.priors = [[0.0,10.0],[0.0,2.0],[50.0,150.0],[10.0,30.0]]
                self.parameters = [sampleuniform(1,self.priors[0][0],self.priors[0][1]),sampleuniform(1,self.priors[1][0],self.priors[1][1]),sampleuniform(1,self.priors[2][0],self.priors[2][1]),sampleuniform(1,self.priors[3][0],self.priors[3][1])]
                self.weight = 1.0/2.0


        def perturbAll(self,kernel):
		self.parameters = [self.perturbation(self.parameters[ind],self.priors[ind],kernel[ind]) for ind in range(4)]
			
		
        def perturbation(self,parameter,prior,kernel):
                lflag = parameter + kernel.lower < prior[0]
                uflag = parameter + kernel.upper > prior[1]
                lower = kernel.lower
                upper = kernel.upper
                if lflag == True:
                        lower = -(parameter - prior[0])
                if uflag == True:
                        upper = prior[1] - parameter
                if uflag == False and lflag == False:
                        delta = sampleuniform(1,lower,upper)
                else:
                         positive = rnd.uniform(0,1) > abs(lower)/(abs(lower)+upper)
                         if positive == True:
                                delta = sampleuniform(1,0,upper)
                         else:
                                delta = sampleuniform(1,lower,0)
                return parameter + delta






	
def pdensity(scale1,scale2,parameter):
        if ((parameter>scale2) or (parameter<scale1)):
                return 0.0
        else:
                return 1.0/float(scale2-scale1)


def sampleuniform(scale,lb,ub):
        return scale*np.random.uniform(lb,ub)



def main():
	pop = populations()
	p1 = particle()
	p2 = particle()
	pop.addToPopulation(p1)
        pop.addToPopulation(p2)
        print pop.particles[0].parameters[0]
        pop.postprocess()
	print len(pop.previous_particles)
	p1.perturbAll(pop.kernels)





	






	





