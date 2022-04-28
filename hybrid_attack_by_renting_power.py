
# The simulation of hybrid attack by renting mining powers

import random
import sys
import numpy as np

# the total hashrate of Bitcoin network (2021-9-13 16:00) is  133731.55 PH/s
network_hashrate = 133731.55

# the proportion of hashrate already owned by the mining pool
haved_hashrate_perchent = 0.1780

# the rented hashrate (percentage of the entire network) to reach the 0.27 power
hashrate_rent_percent = 0.0920

# the rented hashrate (PH/s)
rent_hashrate = hashrate_rent_percent * network_hashrate

# the cost of renting 24 hours of hashrate (with 12.89 dollars 1 hour)
rent_cost = rent_hashrate * 12.89 * 24


# total 100,000 simulations are performed
total_simulate_count = 100000

# current simulation count
simulate_count = 0

# attacker's total hashrate (owned + rented)
mining_power = haved_hashrate_perchent + hashrate_rent_percent


# used to record the results of each simulation for averaging
valid_blocks_of_attacker = np.zeros(total_simulate_count)
relatev_rewards_of_attacker = np.zeros(total_simulate_count)
coin_number_of_attacker = np.zeros(total_simulate_count)
rewards_of_attacker = np.zeros(total_simulate_count)
profit_of_attacker = np.zeros(total_simulate_count)



def average_value(array):
    sum = 0
    for x in array:
        sum += x
    return sum/total_simulate_count



class Hybrid_Selfish_Mining:

    def __init__(self, **d):
        self.__nb_simulations = d['nb_simulations']
        self.__delta = 0 # advance of selfish miners on honest one
        self.__privateChain = 0 # length of private chain RESET at each validation
        self.__publicChain = 0 # length of public chain RESET at each validation
        self.__honestsValidBlocks = 0 # the number of honest miners'  valid blocks
        self.__selfishValidBlocks = 0 # the number of selfish miner's valid blocks
        self.__counter = 1
        self.__alpha = d['alpha']
        self.__gamma = d['gamma']
        self.__publishParam = d['rho'] # param \rho in paper
        # For results
        self.__revenue = None
        self.__orphanBlocks = 0
        self.__totalMinedBlocks = 0 # total valid blocks mined in simulation



    def Simulate(self):

        # Suppose a block is generated in 10 minutes,
        # and 144 blocks are generated in 24 hours
        while((self.__honestsValidBlocks + self.__selfishValidBlocks) <= 144):
            # Mining power does not mean the block is actually found
            # there is a probability p to find it
            r = random.uniform(0, 1)
            self.__delta = self.__privateChain - self.__publicChain
            if r <= float(self.__alpha):
                self.On_Selfish_Miners() # selfish miner mines a new block
            else:
                self.On_Honest_Miners() # honest pool mine a new block

            self.__counter += 1

        # Publishing private chain if not empty when total nb of simulations reached
        self.__delta = self.__privateChain - self.__publicChain
        if self.__delta > 0:
            self.__selfishValidBlocks += self.__privateChain
            self.__publicChain, self.__privateChain = 0,0

        # calculating the selfish miner's relative revenue
        self.actualize_results()

    def On_Selfish_Miners(self):
        self.__privateChain += 1
        if self.__delta == 0 and self.__privateChain == 2:
            self.__privateChain, self.__publicChain = 0,0
            self.__selfishValidBlocks += 2


    def On_Honest_Miners(self):
        self.__publicChain += 1
        if self.__delta == 0:
            # if 1 block is found => 1 block validated as honest miners take advance
            self.__honestsValidBlocks += 1

            s = random.uniform(0, 1)
            if self.__privateChain > 0 and s <= float(self.__gamma):
                self.__selfishValidBlocks += 1
            elif self.__privateChain > 0 and s > float(self.__gamma):
                self.__honestsValidBlocks += 1

            self.__privateChain, self.__publicChain = 0,0

        elif self.__delta == 2:
            self.__selfishValidBlocks += self.__privateChain
            self.__publicChain, self.__privateChain = 0,0

        elif self.__delta > 2:
            rho = random.uniform(0, 1)
            if rho < float(self.__publishParam): # releasing all private blocks with prob \rho
                self.__selfishValidBlocks += self.__privateChain
                self.__publicChain, self.__privateChain = 0, 0

    def actualize_results(self):
        '''
        to calculate the selfish miner's relative revenue
        '''
        # Total Valid Blocks Mined
        self.__totalMinedBlocks = self.__honestsValidBlocks + self.__selfishValidBlocks
        # Orphan Blocks
        self.__orphanBlocks = self.__nb_simulations - self.__totalMinedBlocks

        # selfish miner's  revenue
        if self.__honestsValidBlocks or self.__selfishValidBlocks:

            # to calculate the relative revenue
            self.__revenue =  round(self.__selfishValidBlocks / (self.__totalMinedBlocks), 3)
            # self.__revenue = 100*round(self.__selfishValidBlocks/(self.__totalMinedBlocks),3)

            valid_blocks_of_attacker[simulate_count] = self.__selfishValidBlocks
            relatev_rewards_of_attacker[simulate_count] = self.__revenue
            coin_number_of_attacker[simulate_count] = self.__selfishValidBlocks * 6.25 # 6.25 bitcoins per block
            rewards_of_attacker[simulate_count] = self.__selfishValidBlocks * 6.25 * 46108.37 #  The market value of one bitcoin was $46,108.37.
            profit_of_attacker[simulate_count] = (self.__selfishValidBlocks * 6.25 * 46108.37) - rent_cost


if len(sys.argv) == 1:

    simulate_count = 0

    while simulate_count < total_simulate_count :
        new = Hybrid_Selfish_Mining(**{'nb_simulations': 200000, 'alpha': mining_power, 'gamma': 0.5, 'rho':1.0})
        new.Simulate()
        simulate_count += 1
        print('processed ' + str( (simulate_count/total_simulate_count) * 100 ) + '%')

    print('\n Simulation Results: ')
    valid_blocks_num_average = average_value(valid_blocks_of_attacker)
    print('the average number of valid blocks mined by attacker in 24 hours: \n'\
          + str(valid_blocks_num_average) + '\n')

    print('rental cost: ' + '$' + str(rent_cost) + '\n')

    profit_average = average_value(profit_of_attacker)
    print('net profit: ' + '$' + str(profit_average) + '\n')



