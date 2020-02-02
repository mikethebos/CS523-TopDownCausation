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
    values = [3.9, 4.0]
    return random.choice(values)


def run_sim(eps, x_0, K, N, generations):
    x[:, 0] = x_0
    for n in range(1, generations):
        for i in range(N):
            calc_x_inp1(eps, i, n, K, N)


def calc_M_n():
    return np.average(x, axis=0)


def plot(M, index):
    colors = ['m', 'r', 'b', 'y', 'c', 'g', 'k', 'k']
    x_vals = M[:-1]
    y_vals = M[1:]
    plt.scatter(x_vals, y_vals, c=colors[index])


def main():
    x_0 = 1
    K = 100
    N = 1000
    generations = 10000  # Evenually 10000
    global x
    eps_vals = [0, 0.075, 0.1, 0.2, 0.225, 0.25, 0.3, 0.4]
    for index in range(len(eps_vals)):
        eps = eps_vals[index]
        x = np.zeros((N, generations))
        run_sim(eps, x_0, K, N, generations)
        M = calc_M_n()
        plot(M, index)
        print("Finished epsilon = ", eps)
    plt.title('Map for Varying Values of the Global Coupling Strength')
    plt.xlabel('M_n')
    plt.ylabel('M_n+1')
    plt.rc('font', 22)
    plt.show()


if __name__ == "__main__":
    main()
