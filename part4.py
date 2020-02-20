"""
Author: Justin Deterding
Created: Wed Feb 12 19:28:14 2020
Description:
"""
#%% IMPORTS ===================================================================
from LogisticGrowthModel import generateGrowthModels
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#%% FUNCTION DEFINITIONS ======================================================
def instRepFittnessFun(pops, repFitCoeff, carryCap):
    x = (np.sum(pops) - carryCap)/(carryCap/repFitCoeff)
    return repFitCoeff/(1+np.exp(x)) 
#%%PLOT TO THE REPRODUCTIVE FITTNESS FUNCTION =================================

Rmax = 3.9; carryCap=100

totalpop =np.linspace(0,2*carryCap,100)
plt.figure()
plt.plot(totalpop,[instRepFittnessFun(p,8.0,100) for p in totalpop], label= "$r_{max}$: 8.0 K: 100")
plt.plot(totalpop,[instRepFittnessFun(p,4.0,100) for p in totalpop], label= "$r_{max}$: 4.0 K: 100")
plt.plot(totalpop,[instRepFittnessFun(p,2.0,100) for p in totalpop], label= "$r_{max}$: 2.0 K: 100")
plt.ylabel("Reproductive Fitteness")
plt.xlabel("Total Population")
plt.legend()
#%% PLOT STATIC AND DYNAMIC TIME SERIES ======================================= 
# Initial parameters
Npops = 10
tTotal= 100
repFitCoeffs = np.linspace(0.5,3.33,Npops)
carryCaps    = np.ones((Npops,))*100
Xdynamic = np.zeros(shape=(Npops,tTotal))
#Xstatic  = np.zeros(shape=(Npops,tTotal))
# Initial populations
Xdynamic[:,0] = 1.0
#Xstatic[:,0]  = 1.0
# generate growth models
dynGrowthModels  = generateGrowthModels(carryCaps=np.ones(Npops)*carryCap
                                    ,repFitCoeffs=repFitCoeffs,
                                    repFitFun=instRepFittnessFun)
for t in range(tTotal-1):
    Xdynamic[:,t+1] = dynGrowthModels(Xdynamic[:,t])

fig, axarr = plt.subplots(nrows=3,sharex=True)
plotInx = np.array([3,7,9],dtype=np.int)  
for ax,xdyn,r in zip(axarr,Xdynamic[plotInx],repFitCoeffs[plotInx]):    
    ax.plot(xdyn)
    ax.set_title('Reproductive Coefficent: {:4.2f}'.format(r))
fig.text(0.04, 0.5, 'Individual Population', va='center', rotation='vertical')
ax.set_xlabel('Generation')    
ax.set_ylim(0,100)


#%% Plot bifrication map for small populations
t_transient   = 500
t_steadyState = 300   
Npops         = 10

plt.figure()
plt.xlabel('Reproduction Rate', fontsize=12);
plt.ylabel('Population',fontsize=12);

for rMax in np.linspace(2.0,4.0,4):
   
    repFitCoeffs = np.linspace(0.5,rMax, Npops)

    Xdynamic = np.zeros(shape=(Npops,t_steadyState))

    dynGrowthModels  = generateGrowthModels(carryCaps=np.ones(Npops)*carryCap
                                        ,repFitCoeffs=repFitCoeffs,
                                        repFitFun=instRepFittnessFun)
    Xdynamic[:,0] = 1.0

    for t in range(t_transient):
        Xdynamic[:,0] = dynGrowthModels(Xdynamic[:,0])
    
    for t in range(t_steadyState-1):
        Xdynamic[:,t+1] = dynGrowthModels(Xdynamic[:,t])

    

    rPlot = np.ravel(np.transpose(np.ones(Xdynamic.shape).T*repFitCoeffs))
    xPlot = np.ravel(Xdynamic)
    
    plt.plot(rPlot,xPlot,'-o', markersize=6,
             label = "Max Rep. Rate: {:4.2f}".format(rMax))
    
plt.legend()


#%% Plot bifrication map for Large populations
t_transient   = 10000
t_steadyState = 1000   
Npops         = 500

plt.figure()
plt.xlabel('Reproduction Rate', fontsize=12);
plt.ylabel('Population',fontsize=12);

Rmax = 5.0
   

repFitCoeffs = np.linspace(0.5,Rmax, Npops)

Xdynamic = np.zeros(shape=(Npops,t_steadyState))

dynGrowthModels  = generateGrowthModels(carryCaps=np.ones(Npops)*carryCap
                                    ,repFitCoeffs=repFitCoeffs,
                                    repFitFun=instRepFittnessFun)
Xdynamic[:,0] = 1.0

for t in range(t_transient):
    Xdynamic[:,0] = dynGrowthModels(Xdynamic[:,0])

for t in range(t_steadyState-1):
    Xdynamic[:,t+1] = dynGrowthModels(Xdynamic[:,t])

rPlot = np.ravel(np.transpose(np.ones(Xdynamic.shape).T*repFitCoeffs))
xPlot = np.ravel(Xdynamic)

plt.plot(rPlot,xPlot,'o', markersize=1, alpha=0.01)
    

#%%
bool1 = np.zeros(repFitCoeffs.shape,dtype=np.int)
bool2 = np.zeros(repFitCoeffs.shape,dtype=np.int)
bool1[repFitCoeffs>3.2]=1
bool2[repFitCoeffs<4.5]=1
plotBool = bool1*bool2

instTotalPop = np.sum(Xdynamic, axis=0)

fix, axarr = plt.subplots(ncols=2)
numToPlot = 4; N = 0; lines = []; labels = []
for b,x,r in zip(plotBool[::25],Xdynamic[::25,:], repFitCoeffs[::25]):
    if b:
        li, = axarr[1].plot(x[:-1],x[1:],'o', markersize=2)
        lines.append(li); labels.append("r: {:4.2f}".format(r))

axarr[1].plot(np.linspace(0.0,np.max(Xdynamic)),
              np.linspace(0.0,np.max(Xdynamic)),'--k')
axarr[0].plot(np.linspace(0.0,np.max(instTotalPop)),
              np.linspace(0.0,np.max(instTotalPop)),'--k')
      
        
plt.legend(lines,labels)
axarr[1].set_title('Individual \n Populations')
axarr[0].set_title('Total \n Population')

axarr[0].plot(instTotalPop[:-1],instTotalPop[1:],'o', markersize=2,  label="Total Population")
axarr[0].set_xlabel('$X_i$')
axarr[0].set_ylabel('$X_{i+1}$')
axarr[1].set_xlabel('$X_i$')
axarr[1].set_ylabel('$X_{i+1}$')

#%%
maxPopInx = np.unravel_index(np.argmax(Xdynamic, axis=None), Xdynamic.shape)

plt.figure()
normTotal = instTotalPop/instTotalPop.max()
for pltInx in [maxPopInx[0]-20,maxPopInx[0],maxPopInx[0]+20]:
    normX = Xdynamic[pltInx,:]/Xdynamic[pltInx,:].max()
    xplot = (normX-normTotal)/(normX+normTotal)*200
    plt.plot(xplot, label="r: {:4.2f}".format(repFitCoeffs[pltInx]))
plt.legend()
plt.xlabel("Generation")
plt.ylabel("Percent Difference \n from Total Population")

#%% "animation"
"""
Npops = 5
repFitCoeffs =np.linspace(1.0,3.0,Npops)

#-----------
fig, ax = plt.subplots()


x = np.ones(shape=(Npops,))       # Initial polulations
line, = ax.plot(repFitCoeffs, x, 'o')

max_pop = 0.0
for i in range(300):
    #print("Current Generation: {}".format(i*100))
    x = dynGrowthModels(x)
    if np.max(x)> max_pop:    
        max_pop = np.max(x)
        ax.set_ylim(0.0,max_pop)
    line.set_ydata(x)
    plt.show()
    plt.pause(.01)

#plt.show()
"""




