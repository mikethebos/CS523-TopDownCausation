"""
Author: Justin Deterding
Created: Sat Feb  1 13:20:55 2020
Description:
"""

import numpy as np

def globalLogisticGrowth(currPops ,growthModels ,couplingCoeff, args=None):
    """
    globalLogisticGrowth is equation (1) from "Evolutionary Transitions and 
    Top-Down Causation" describing the global dynamics of the logistic growth 
    of coupled populations with independent growth models.

    Parameters
    ----------
    currPops : (N,) array_like
        The current population of the system, where each row is an individual 
        population.
    growthModels : function
        growthModels is a function where when X_i is the vector representing the
        current population then, X_i+1 = growthModels(X_i,*args). For 
        convenience see generateGrowthModels in this module for generating this
        function.
    couplingCoeff : double
        A value in the range [0,1] representing the coupling to the populations
    args: tuple, optional
        arguments to be passed to the growthModels function.
        
    Returns
    -------
    (N,) array_like
        The next population in the globalLogisticGrowth.
    """
    assert couplingCoeff>=0 and couplingCoeff<=1
    if args:
        nextPops = growthModels(currPops,*args)
    else:
        nextPops = growthModels(currPops)
    return (1-couplingCoeff)*nextPops+couplingCoeff*np.average(nextPops) 

def localLogisticGrowth(currPop, repFitCoeff, carryCap):
    """
    localLogisticGrowth is equation (2) rom "Evolutionary Transitions and 
    Top-Down Causation" describing the local dynamics of a particular population

    Parameters
    ----------
    currPop : double
        value representing the current population (x_n).
    repFitCoeff : double
        reproductive fittness (r) coefficent.
    carryCap : double
        carrying capacity (K) coefficent.

    Returns
    -------
    double 
        next generations population (x_n+1)
    """
    
    return repFitCoeff*(currPop-currPop**2/carryCap)

def generateGrowthModels(repFitCoeffs, carryCaps):
    """
    generateGrowthModels gennerates the growthModels variable for use in the 
    globalLogisticGrowth equation. Currently it takes two list of equal length
    and creates a function to compute N growth models. When the length of the 
    input vector should be the number of local models.
    In the language of "Evolutionary Transitions and Top-Down Causation"...
    x_1,n+1    f(x_1,n,r_1,K_1)
    x_2,n+1 =  f(x_2,n,r_2,K_2)
     ...       ...
    x_N,n+1    f(x_N,n,r_N,K_N)
    
    Parameters
    ----------
    repFitCoeffs : (N,) array-like
        reproductive fittness coefficent (r_i) for the ith logistic model.
    carryCaps : (N,) array-like
       carrying capacity coeffiecent (K_i) for the ith logistic model 

    Returns
    -------
    function
        a function with a single vector argument for the current population. 
        X_n+1 = f(X_n)

    """
    assert len(repFitCoeffs)==len(carryCaps)
    return lambda pops:np.array([localLogisticGrowth(p,r,k) for p,r,k in zip(pops,repFitCoeffs,carryCaps)])

def instDynamicMeanFeild(currPops,growthModels):
    """
    istDynamicMeanFeild is equation (4) from "Evolutionary Transitions and 
    Top-Down Causation". It calculates the instintanious dynamics of the mean 
    feild M_n.
    
    Parameters
    ----------
    currPops : (N,) array_like
        The current population of the system, where each row is an individual 
        population.
    growthModels : function
        growthModels is a function where when X_i is the vector representing the
        current population then, X_i+1 = growthModels(X_i,*args). For 
        convenience see generateGrowthModels in this module for generating this
        function.

    Returns
    -------
    double 
        instintanious dynamics of the mean feild M_n.

    """
    return np.average(growthModels(currPops)) 

def instMeanFeild(currPops):
    """
    instMeanFeild is equation (3) from "Evolutionary Transitions and 
    Top-Down Causation". It calculates the instintanious state of the entier 
    system.
    
    Parameters
    ----------
    currPops : (N,) array_like
        The current population of the system, where each row is an individual 
        population.
        
    Returns
    -------
    double
        nstintanious state of the entier system.
    """
    return np.average(currPops)





