# CS523-TopDownCausation
Project for CS523 for recreating the results of Evolutionary Transitions and Top-Down Causation.

## For generating part 2:
The file logistic_map.py was used for generating results in both part 2 and part 3.  In the last line of the program if pic = True then it generates the return map figure for 1000 populations and 10000 generations, with global coupling strengths following the values used in the Walker paper.  The directory 'logistic_map_figures' contains 10 figures generated with the best-fit figure shown in our paper. 

## For generating part 3: 
The file logistic_map.py with the last line setting pic = False generates data for 10 metapopulations, each with 3 subpopulations sampled from 1000 subpopulations with 1000 generations.  The global coupling strengths are from values 0 to 1 incremented by 0.025.  After this population data was generated, the MatLab file TEcalc.m was used to calculate the transfer entropy in both directions and stores it as 'TD_data.csv' and 'BU_data.csv'.  The MatLab file plotCI.m reads in these files, calculates the average and 95% confidence intervals, and creates the final plot used in our project.  The MatLab file MIcalc.m reads in the population data and computes the mutual information between sub-populations and produces the plot used in the project.  
