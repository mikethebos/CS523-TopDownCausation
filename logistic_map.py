import random
import numpy as np
from matplotlib import pyplot as plt

# The model calculated at population i generation n+1.  
def calc_x_inp1(eps, i, n, K, N):
    x[i, n] = (1-eps)*calc_f(x[i, n-1], K) + eps*calc_m_n(N, n-1, K)

# Local dynamics of a population i at generation n, the discrete logistic map
def calc_f(x_val, K):
    return get_r()*x_val*(1-(x_val/K))

# The instantaneous mean field 
def calc_M_n():
    return np.average(x, axis=0)

# The dynamics of the instantaneous mean field
def calc_m_n(N, n, K):
    return np.average(calc_f(x[:, n], K))

# Sampling of r in the chaotic regime, random.uniform provides an independent 
# uniform distribution between 3.9 and 4.0
def get_r():
    return random.uniform(3.9, 4.0)

# Runs the simulation for the specified parameters, sets the initial generation
def run_sim(eps, x_0, K, N, generations):
    x[:, 0] = x_0
    for n in range(1, generations):
        for i in range(N):
            calc_x_inp1(eps, i, n, K, N)

# Makes the scatter plot, 
def plot(M, index):
    colors = ['m', 'r', 'b', 'y', 'c', 'g', 'k', 'k']
    x_vals = M[:-1]
    y_vals = M[1:]
    if index == 6:
        mark = '*'
        s = 15
    else:
        mark = 'o'
        s = 1
    plt.scatter(x_vals, y_vals, c=colors[index], marker=mark, s=s)

# Sets plotting parameters and adds a logistic map 
def plotspecs():
    xmin = 40
    xmax = 80
    plt.title('Map for Varying Values of the Global Coupling Strength')
    plt.xlabel('$M_n$')
    plt.ylabel('$M_{n+1}$')
    plt.xlim([xmin, xmax])
    plt.ylim([xmin, xmax])
    plt.rcParams.update({'font.size': 9})
    plt.plot([xmin, xmax], [xmin, xmax], 'k-')
    x = np.linspace(0, 1)
    plt.plot(x*100, get_r()*x*(1-x)*100, 'g', LineWidth=3)
    plt.show()
    # sts = "logmap_iter" + str(iteration) + "_" + str(x_0) + ".png"
    # plt.savefig(sts)

# Used for part 3 to generate 3 samples of populations from the metapopulation
# Saves each file with the first column as the instantaneous mean field and 
# the second, third, and fourth as the population data for all generations, 
# Also stores all values rounded to the nearest integer to use the discrete
# value transfer entropy tool. 
def storedata(xtrans, M, N, gens, index, metapop):
    sample = np.random.choice(xtrans.shape[1], 3, replace=False)
    print(sample)
    chosenpops = xtrans[:, sample]
    dataarray = np.zeros((gens, 4))
    dataarray[:, 0] = M
    dataarray[:, 1:] = chosenpops
    # print(np.round(dataarray))
    np.savetxt("TEdata/MX_" + str(index) + '_' + str(metapop) + ".csv",
               np.round(dataarray), fmt='%d', delimiter=',')

# Sets parameters.  If part 2 (pic=True) runs the simulation for all epsilon
# and plots the figure.  If part 3 runs the simulation and stores the 3 
# sampled populations.  
def main(x_0, eps_vals, pic=False):
    K = 100
    N = 1000
    metapops = 10  # For part 3
    generations = 1000 # For part 3
    global x
    if pic:
        plt.clf()
        metapops = 1  # For part 2
        generations = 10000  # For part 2
    for index in range(1,2): #range(len(eps_vals)):
        eps = eps_vals[index]
        print(eps)
        for metapop in range(metapops):
            x = np.zeros((N, generations))
            run_sim(eps, x_0, K, N, generations)
            M = calc_M_n()
            if not pic:
                storedata(np.transpose(x), M, N, generations, index, metapop)
            if pic:
                plot(M, index)
        print("Finished epsilon = ", eps)
    if pic:
        plotspecs()

# If part 2 sets epsilon values to match Walker.  If part 3 sets epsilon values
# to be between 0 and 1 at 0.025 increments. 
if __name__ == "__main__":
    eps_vals_pic = [0, 0.075, 0.1, 0.2, 0.225, 0.25, 0.3, 0.4]
    eps_vals = np.arange(0, 1.025, 0.025).tolist()
    x0 = 1
    main(x0, eps_vals_pic, pic=True)
