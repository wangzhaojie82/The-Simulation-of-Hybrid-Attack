
# To solve the Markov problem:
# 1. solving the stationary distribution of the hybrid attack 
#

import numpy as np

np.set_printoptions(suppress=True) # Not use scientific notation when suppress=True.

def solving_markov_chain(N, alpha, rho):
    '''
    To solve the Markov Problem of Hybrid Attack .
    :param N: the number of states in the hybrid attack
    :param alpha: the mining power of the attacker
    :param rho: the publish param \rho in the paper
    :return real: The list of stationary distribution
    '''

    # Initialize the transition matrix by zeros
    QT = np.zeros((N, N))

    # Fill the transition matrix with true probability values
    QT[0, 0] = 1 - alpha
    QT[0, 2] = alpha

    QT[1, 0] = 1 # means state 0' to state 0 with probability 1 = alpha + (1-alpha)gamma + (1-alpha)(1-gamma)

    QT[2, 1] = 1 - alpha
    QT[2, 3] = alpha
    QT[3, 0] = 1 - alpha
    QT[3, 4] = alpha
    QT[4, 0] = (1 - alpha) * rho
    QT[4, 3] = (1 - alpha) * (1 - rho)
    QT[4, 5] = alpha
    QT[5, 0] = (1 - alpha) * rho
    QT[5, 4] = (1 - alpha) * (1 - rho)
    QT[5, 6] = alpha
    QT[6, 0] = (1 - alpha) * rho
    QT[6, 5] = (1 - alpha) * (1 - rho)
    QT[6, 6] = alpha



    # Find the eigenvalues and eigenvectors
    evals, evecs = np.linalg.eig(QT.T) 

    # Find the stationary distribution 
    # The station is a column vector, you can find it by station.shape
    station = evecs[:, np.isclose(evals, 1)]


    station_normal = station.T / station.T.sum()  # normalization

    real = real_station(station_normal) # Format the data

    print('\n')
    print('Method: MarkovChainSolver.solving_markov_chain() ')
    print('Params: [N = ' + str(N) + ', alpha = ' + str(alpha) + ', rho = ' + str(rho) + ']')
    print('State sequence: [0, 0\', 1, 2, 3, 4, 5]')
    print('Station distribution: ' + str(real))
    print('\n')


    return real


def real_station(station):
    '''
    Convert the complex number form (in the stationary distribution) to the real number form
    :param station: the stationary distribution (a column vector) to be converted
    :return: the stationary distribution composed of real numbers
    '''
    station_real_form = []
    i=0
    while i < station.shape[1]:
        #print(i)
        number = round(station[0,i].real, 6)
        station_real_form.append(number)
        i += 1

    return station_real_form



def specific_params():
    # Initialize the constants
    N = 7  # the num of state: [0, 0', 1, 2, 3, 4, 5]
    alpha = 0.3  # the mining power of attacker
    rho = 0.8   # hybrid attack publish param

    solving_markov_chain(N, alpha, rho)



def dynamic_params():
    # Initialize the constants
    N = 7  # the num of state: [0, 0', 1, 2, 3, 4, 5]
    # alpha = 0.25  # the mining power of attacker
    # rho = 0.5   # hybrid attack publish param

    alphas = np.arange(0, 50, 10) / 100
    rhos = np.arange(0, 11, 1) / 10

    percentage = 0  # percentage done

    for alpha in alphas:
        for rho in rhos:
            solving_markov_chain(N, alpha, rho)

            percentage += (1 / (len(alphas) * len(rhos)))
            print("progress : " + str(round(percentage, 2) * 100) + "%\n")


if __name__ == '__main__':

    specific_params() # the stationary distribution of specific (fixed) parameters
    # dynamic_params() # the stationary distribution of dynamic (vary) parameters


