"""
This script simulates a directed percolation process.
The updating strategy is described in detail in the function descriptions.
The density over time date for every run is automatically stored in a csv file in the project directory.
For postprocessing, look into `evalruns.py`
"""
import random
import numpy as np
import os
from datetime import datetime
import csv


def update(sites, prob):
    """
    updates the state of a row according to the following update rule:
    -- s_i is influenced by the former state of s_i and s_(i+1) ("neighbours" in a time-sense)
    -- s_i becomes infected/wet with probability p for every connection to an already infected neighbour
    :param sites: 1D numpy array, list of 0's or 1's depending on the state of the site
    :param prob: float, probability for open bonds
    :return: 1D numpy array, updated row of length len(S)
    """
    size = len(sites)  # number of sites to get the connections right
    newlist = np.zeros(size)
    for i in range(size):
        # get a 1 only if:
        # 1) a neighbour is infected
        # 2) the probability function returns 1 rather than 0
        newlist[i] = (random.random() < prob and sites[i]) or random.random() < prob and sites[(i + 1) % size]
    return newlist


def density(lattice):
    """
    :param lattice: 1D numpy array, current sites chain
    :return: float, the density of a row of sites, in our case simply the number of ones in `sites`
    """
    return sum(lattice) / len(lattice)


def singleRun(latsize, numiter, prob):
    """
    performs a single simulation run
    :param latsize: int, size of the 1D lattice
    :param numiter: int, number of iterations
    :param prob: float, existing bond probability
    :return: 1D numpy array of size numiter, containing the density at each time step
    """
    lattice = np.array([1] * latsize)  # initialize lattice
    densities = np.zeros(numiter + 1)  # create density array of proper size to prevent "append" usage
    densities[0] = density(lattice)  # insert initial density
    for j in range(numiter):
        lattice = update(lattice, prob)
        dens = density(lattice)
        densities[j+1] = dens
    return densities


if __name__ == "__main__":
    ########################
    # simulation parameters
    ########################
    N = 1000  # lattice size
    T = 1000  # number of iterations per run
    M = 10000  # number of runs
    p = 0.6447  # infection probability
    ########################
    # csv file parameters
    ########################
    alldens = [0] * M   # matrix to store the density arrays of all runs
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # path to file to store the density information for all runs, by default in project directory
    filename = 'perco_p%f_N%d_T%d_M%d_%s.csv' % (p, N, T, M, datetime.now().strftime("%H--%M--%S"))
    filepath = os.path.join(root_dir, filename)
    print(filepath)
    #########################
    # start procedure
    #########################
    starttime = datetime.now()
    f = open(filepath, 'w', newline='')
    csvwrite = csv.writer(f)
    currentdens = []  # storage for the current run's density array
    for numrun in range(M):  # perform m runs
        currentdens = singleRun(N, T, p)  # get the current run's density info
        alldens[numrun] = currentdens
        csvwrite.writerow(currentdens)
        print("Finished run %d / %d" % (numrun + 1, M))
    f.close()  # close csv file
    endtime = datetime.now()
    print("End of simulation! Elapsed time: %s" % (endtime-starttime))
