"""
Author: Justin Deterding
Created: Thu Feb  6 15:28:56 2020
Description:
"""
#%% Imports
import numpy as np
import matplotlib.pyplot as plt
from LogisticGrowthModel import localLogisticGrowth

#%% Parameters
N_generations = 100
N_populations = 4
carryingCapacity = 100 

#R = np.array([2.9,3.0,3.1,3.2])
R = np.array([2.9,2.9,3.7,3.7])
K = np.ones((N_populations,))*carryingCapacity
X = np.zeros(shape=(N_populations,N_generations))
# Initial Populations
X[:,0] = np.array([1.0,1.1,1.0,1.1])

#%% popigate the generations
for gen in range(N_generations-1):
    X[:,gen+1] = localLogisticGrowth(X[:,gen],R,K)

#%% Plotting

fig = plt.figure()
for x,r in zip(X,R):
    plt.plot(x,'o',markersize=4, label='r: {:2.1f}'.format(r))
plt.hlines(carryingCapacity,-10,N_generations+10,linestyles="dashed", label="Carrying Capacity")
plt.xlabel('time/generations', fontsize=12)
plt.ylabel('Population', fontsize=12)
plt.xlim(0,N_generations)
plt.ylim(0,carryingCapacity)
plt.legend(fontsize=12)
    





