"""
This script is used to read in a previously (using the `runsim.py` - script) created csv file
(the path has to be changed by hand in the first line of this script's main function!) containing the density values
for a certain amount of directed percolation runs.
Here, the density over time is plotted for the very last run (arbitrarily chosen) and furthermore,
the mean density over all runs is plotted as a function of time.
"""
import numpy as np
import csv
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # this path needs to be changed locally
    # filepath = "C:\\Users\\ivayl\\PycharmProjects\\Percolation\\perco_p0.644700_N1000_T1000_M100_17--41--10.csv"
    filepath = "C:\\Users\\ivayl\\PycharmProjects\\Percolation\\perco_p0.644700_N1000_T1000_M1000_18--18--47.csv"

    ###################################################
    # read csv file containing density info of all runs
    ###################################################
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        alldens = np.array([list(map(float, row)) for row in reader])

    ###############################################
    # density over time plot, just for the last run
    ###############################################
    lastrun = alldens[-1]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.suptitle(r'$\rho$(t) for single run with p = %f, N = %d, T = %d' % (p, N, T))
    fig.suptitle(r'$\rho$(t) for last run')
    # standard plot on axis 1
    ax1.plot(lastrun, 'x')
    ax1.set_xlabel("time step t", fontsize=14)
    ax1.set_ylabel(r'$\rho$(t)', fontsize=14)
    ax1.yaxis.labelpad = -10
    # loglog plot on axis 2
    ax2.loglog(lastrun, 'x')
    ax2.set_xlabel("time step t", fontsize=14)
    ax2.set_ylabel(r'$\rho$(t)', fontsize=14)
    ax2.yaxis.labelpad = -20
    plt.show()

    ######################################################
    # mean density over all runs
    ######################################################
    # we have a matrix with the row i corresponding to the density information of run number i + 1 (bc. we start at 0)
    column_means = alldens.mean(axis=0)  # column-wise mean value gives the mean for each time step
    figM, axM = plt.subplots()
    axM.loglog(column_means, 'x')
    axM.set_xlabel("time step t", fontsize=14)
    axM.set_ylabel(r'$\rho_{mean}$(t)', fontsize=14, va='top')
    plt.show()
