"""
Author: Justin Deterding
Created: Thu Feb  6 15:28:56 2020
Description:
"""
#%% Imports
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from LogisticGrowthModel import localLogisticGrowth
from matplotlib.patches import Circle
#%% FUNCTION DEFINITIONS
def generatePDFs(X,numberOfBins,binRange=None):
    if not binRange:
       binRange=(X.min(),X.max())
    bins             = np.linspace(*binRange,numberOfBins)
    binAssignments   = np.digitize(X,bins)
    prob = np.ones(shape=(X.shape[0],numberOfBins))
    for inx,popBinAssignment in enumerate(binAssignments):
        for binNumber in range(1,numberOfBins):
           prob[inx,binNumber] = np.sum(popBinAssignment==binNumber)/X.shape[1] 
    return prob
def generateJointPDF(xt,yt,NXbins,NYbins,XbinRange=None,YbinRange=None):
    if not XbinRange:
        XbinRange = (xt.min(),xt.max())
    if not YbinRange:
        YbinRange = (yt.min(),yt.max())
    xbins            = np.linspace(*XbinRange,NXbins+1)
    ybins            = np.linspace(*YbinRange,NYbins+1)
    xtBinAssignments = np.digitize(xt,xbins)
    ytBinAssignments = np.digitize(yt,ybins)
    jointPDF         = np.zeros((NXbins,NYbins))
    Xbins, Ybins     = np.meshgrid(np.arange(1,NXbins),np.arange(1,NXbins))
    for xi, yi in zip(xtBinAssignments,ytBinAssignments):
        Xbool = np.zeros(Xbins.shape);      Ybool = np.zeros(Ybins.shape); 
        Xbool[Xbins==xi]=1;                 Ybool[Ybins==yi]=1;
        jointPDF +=Xbool*Ybool
    jointPDF = jointPDF/len(xt)
    return jointPDF
    
def entropy(pdf,axis=1):
    with np.errstate(all='ignore'):
        return -1.0*np.sum(np.nan_to_num(pdf*np.log2(pdf)),axis=axis)
#%%
font = {'family' : 'normal',
        'size'   : 12}
mpl.rc('font', **font)



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
# bin discritization for use with JIDT tool
numberOfBins    = 10
binRange        = (0.0,carryingCapacity)
bins            = np.linspace(*binRange,numberOfBins)
binAssignments  = np.digitize(X,bins)
# Sanity check
# Calc pobability dist.
fullTimeSeries_pdfs  = generatePDFs(X,numberOfBins,binRange)
firstNtimesteps_pdfs = generatePDFs(X[:,:N],numberOfBins,binRange)
lastNtimesteps_pdfs  = generatePDFs(X[:,-N:],numberOfBins,binRange)
print("Shannon entropyies:")
print(entropy(fullTimeSeries_pdfs))
HofFirstN  = entropy(firstNtimesteps_pdfs)
HofLastN   = entropy(lastNtimesteps_pdfs)
# Joint probabilities
#xt = np.random.rand(100)*100   ***NEEDS MORE TESTING***
#yt = np.random.rand(100)*100
#jointPDF = generateJointPDF(xt,yt,10,10,(0,100),(0,100))

#%% Save Datae to text for calculations
np.savetxt('fullTimeSeries.txt',binAssignments.T,fmt='%d')    
np.savetxt('firstNtimesteps.txt',binAssignments[:,:N].T,fmt='%d')    
np.savetxt('lastNtimesteps.txt',binAssignments[:,-N:].T,fmt='%d')    
#%% Plotting
fig = plt.figure()
plt.plot(Xdiff[0,:],'o')
plt.plot(Xdiff[1,:],'o')
    
#%% time series plots  
fig, axarr = plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(3,2))

axarr[0].plot(X[0,:],'--o',markersize=6, label='$x_0$:{:3.2f} r: {:2.1f}'.format(X[0,0],R[0]))
axarr[0].plot(X[1,:],'--o',markersize=3, label='$x_0$:{:3.2f} r: {:2.1f}'.format(X[1,0],R[1]))
axarr[1].plot(X[2,:],'--o',markersize=6, label='$x_0$:{:3.2f} r: {:2.1f}'.format(X[2,0],R[2]))
axarr[1].plot(X[3,:],'--o',markersize=3, label='$x_0$:{:3.2f} r: {:2.1f}'.format(X[3,0],R[3]))


axarr[0].hlines(carryingCapacity,-10,N_generations+10,linestyles="dashed", label="Carrying Capacity")
axarr[1].hlines(carryingCapacity,-10,N_generations+10,linestyles="dashed", label="Carrying Capacity")

axarr[1].set_xlabel('Generations', fontsize=12)
axarr[0].set_ylabel('Non-Chaotic \n Population', fontsize=12)
axarr[1].set_ylabel('Chaotic \n Population', fontsize=12)
axarr[1].set_xlim(0,N_generations)
axarr[0].set_xlim(0,N_generations)
axarr[1].set_ylim(0,carryingCapacity+10)
axarr[1].set_ylim(0,carryingCapacity+10)
axarr[0].legend(fontsize=12)
axarr[1].legend(fontsize=12)
    
#%% Make Venn diagram
# Inputs       First N time steps          Last  N time steps
#             Non-Chaotic   Chaoti        Non-Chaotic  Chaotic          
Xentropies = [HofFirstN[0], HofFirstN[2], HofLastN[0], HofLastN[2]]  
Yentropies = [HofFirstN[1], HofFirstN[3], HofLastN[1], HofLastN[3]]  
mutualInfo = [2.0419,       2.3899,      0.0,         1.4716]
titles=['First {} Non-Chaotic','First {} Chaotic',
        'Last {} Non-Chaotic', 'Last {} Chaotic']
fig, axarr = plt.subplots(nrows=2, ncols=2, figsize=(8,8)) 

for ax,hx,hy,mi,ti in zip(np.ravel(axarr),Xentropies,Yentropies,mutualInfo,titles):
    
    venX = Circle((hx/2-mi/2,0),hx/2, 
                  alpha =0.1, color ='red', label='H(X)')
    venY = Circle((-hy/2+mi/2,0),hy/2, 
                  alpha =0.1, color ='blue', label='H(Y)')
    mutI = Circle((0,0),1,alpha =0.1, color='purple',label='I(X,Y)')
    ax.add_artist(venX);    ax.add_artist(venY);    #ax.text(0,0,'I(X;Y)')
    ax.set_title(ti.format(N))
    
    
    plt.legend(handles = [venX,venY,mutI])
    ax.set_xlim(-hy+mi/2,hx-mi/2)
    ax.set_ylim(max(hy,hx)/2,max(hy,hx)/-2)
    ax.axis('off')
    
    
    
    
    
    
    
    
    
    
