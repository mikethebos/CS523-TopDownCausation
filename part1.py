"""
Author: Justin Deterding
Created: Thu Feb  6 15:28:56 2020
Description:
"""
#%% Imports
import numpy as np
import matplotlib.pyplot as plt
from LogisticGrowthModel import localLogisticGrowth
from matplotlib.patches import Circle
#%% FUNCTION DEFINITIONS
def entropy(pdf,axis=1):
    with np.errstate(all='ignore'):
        return -1.0*np.sum(np.nan_to_num(pdf*np.log2(pdf)),axis=axis)


#%% Parameters
N_generations = 100
N_populations = 4
carryingCapacity = 100

#R = np.array([2.9,3.0,3.1,3.2])
R = np.array([2.9,2.9,3.7,3.7])
K = np.ones((N_populations,))*carryingCapacity
X = np.zeros(shape=(N_populations,N_generations))
# Initial Populations
X[:,0] = np.array([1.0,1.01,1.0,1.01])

#%% popigate the generations
for gen in range(N_generations-1):
    X[:,gen+1] = localLogisticGrowth(X[:,gen],R,K)
#%% Usefull calculations
# Calculate the diff between the two pop to determine divergence    
Xdiff = np.array([np.abs(X[0,:]-X[1,:]),np.abs(X[2,:]-X[3,:])])
N = 15 # This by observation of looking at resulting plots
# Calc pobability dist.
numberOfBins        = 10
bins                = np.linspace(0.0,carryingCapacity,numberOfBins)
allBinAssignments   = np.digitize(X,bins)
# Probability disribution for the first N
prob = np.ones(shape=(N_populations,numberOfBins))
for inx,popBinAssignment in enumerate(allBinAssignments[:,:N]):
    for binNumber in range(numberOfBins):
       prob[inx,binNumber] = np.sum(popBinAssignment==binNumber)/N 
# Sanity check
print("Shannon entropyies:")
print(entropy(prob))

#%% Save Datae to text for calculations
np.savetxt('fullTimeSeries.txt',allBinAssignments.T,fmt='%d')    
np.savetxt('firstNtimesteps.txt',allBinAssignments[:,:N].T,fmt='%d')    
np.savetxt('lastNtimesteps.txt',allBinAssignments[:,-N:].T,fmt='%d')    
#%% Plotting
fig = plt.figure()
plt.plot(Xdiff[0,:],'o')
plt.plot(Xdiff[1,:],'o')
    
#%% time series plots  
fig = plt.figure()
for x,r,x0 in zip(X,R,X[:,0]):
    plt.plot(x,'o',markersize=4, label='x0:{:3.2f} r: {:2.1f}'.format(x0,r))
plt.hlines(carryingCapacity,-10,N_generations+10,linestyles="dashed", label="Carrying Capacity")
plt.xlabel('Generations', fontsize=12)
plt.ylabel('Population', fontsize=12)
plt.xlim(0,N_generations)
plt.ylim(0,carryingCapacity)
plt.legend(fontsize=12)
    
#%% Make Venn diagram
fig, ax = plt.subplots(figsize=(4,4)) 
entropyX = 3.0
entropyY = 4.0
mutualInfo = 3.0
scale = 1.0

venX = Circle((entropyX/2-mutualInfo/2,0),
              entropyX/2*scale, 
              alpha =0.1, color ='red')
venY = Circle((-entropyY/2+mutualInfo/2,0),
              entropyY/2*scale, alpha =0.1, color ='blue')
ax.add_artist(venX)
ax.add_artist(venY)
ax.set_xlim(-2*max(entropyY,entropyX),2*max(entropyY,entropyX))
ax.set_ylim(-2*max(entropyY,entropyX),2*max(entropyY,entropyX))
