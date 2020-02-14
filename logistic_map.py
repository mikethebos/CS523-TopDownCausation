import random
import numpy as np
from matplotlib import pyplot as plt


def calc_x_inp1(eps, i, n, K, N):
    x[i, n] = (1-eps)*calc_f(x[i, n-1], K) + eps*calc_m_n(N, n-1, K)


def calc_f(x_val, K):
    return get_r()*x_val*(1-(x_val/K))


def calc_m_n(N, n, K):
    return np.average(calc_f(x[:, n], K))


def get_r():
    return random.uniform(3.9, 4.0)


def run_sim(eps, x_0, K, N, generations):
    x[:, 0] = x_0
    for n in range(1, generations):
        for i in range(N):
            calc_x_inp1(eps, i, n, K, N)


def calc_M_n():
    return np.average(x, axis=0)


def plot(M, index):
    colors = ['m', 'y', 'r', 'b', 'c', 'g', 'k', 'k']
    x_vals = M[:-1]
    y_vals = M[1:]
    if index == 6:
        mark = '*'
        s = 15
    else:
        mark = 'o'
        s = 3
    plt.scatter(x_vals, y_vals, c=colors[index], marker=mark, s=s)


def storedata(xtrans, M, N, gens, index, metapop):
    chosenpops = xtrans[:, np.random.choice(xtrans.shape[1], 3, replace=False)]
    dataarray = np.zeros((gens, 4))
    dataarray[:, 0] = M
    dataarray[:, 1:] = chosenpops
    print(dataarray)
    np.savetxt("TEdata/MX_" + str(index) + '_' + str(metapop) + ".csv",
               dataarray, delimiter=',')


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


def main(x_0, eps_vals, pic=False):
    K = 100
    N = 10
    generations = 1000  # 10000
    global x
    if pic:
        plt.clf()
    for index in range(len(eps_vals)):
        eps = eps_vals[index]
        for metapop in range(10):
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


if __name__ == "__main__":
    eps_vals_pic = [0, 0.2, 0.075, 0.1, 0.225, 0.25, 0.3, 0.4]
    eps_vals = np.arange(0, 1.1, 0.1).tolist()
    x0 = 1
    main(x0, eps_vals)
