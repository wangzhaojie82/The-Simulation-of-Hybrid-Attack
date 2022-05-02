# The-Simulation-of-Hybrid-Attack

This is the implementation of the paper *To be detected or not: A Hybrid Selfish Mining Attack*. 



### Scripts list:

- hybrid_attack_simulation.py: The implementation of hybrid attack (or one-time releasing).
- MarkovChainSolver.py: To solve the state probability distribution of hybrid attack (or one-time releasing).
- hybrid_attack_by_renting_power.py: To simulate a mining pool launches a hybrid attack by renting power.



## Hybrid Attack

### Basic Usage

Run `hybrid_attack_simulation.py`, you can simulate an attacker launching the hybrid selfish mining attack in Bitcoin. The attacker's mining power (parameter alpha) varies from 0 to 0.49 by step 0.01. Then, for each fixed alpha and other parameters, the simulation run 200,000 rounds. The results (e.g. attacker's relative revenue) of the simulation will be written to the file 'results.txt'.

*parameters*:

- *nb_simulations*: the total rounds for one simulation,  where one new block is mined in each round.
- *alpha*: attacker's mining power
- *gamma*: the follower fraction of honest miners when blockchain forks
- *rho*: attacker publishes all blocks from the private chain with probability *rho*. If you simulate the one-time releasing attack, this param should be set to 1.

You may want to try out different configurations or other attack strategies.  If so, you can rework the class *Hybrid_Selfish_Mining*, and then run it.  



### More details about the script

The python class *Hybrid_Selfish_Mining* defines the variables and functions used to implement the simulation. You should instantiate a python object with given parameters, then call its Simulate() function to run the simulation, when done, the function write_file() is called to write results to your local storage with a given format.

The functions defined in class *Hybrid_Selfish_Mining*: 

- *Simulate()*: Use a while loop to simulate rounds in block mining. In each loop (round), a random number between 0 and 1 is uniformly sampled, if the number is below param alpha, the function On_Selfish_Miners() is called, otherwise On_Honest_Miners().
- *On_Selfish_Miners()*: simulate attacker's reaction when (s)he mines a block
- *On_Honest_Miners()*: simulate attacker's reaction when other honest miners mine a block
- *actualize_results()*: to calculate the attacker's relative reward when the simulation done.





## State Distribution

To solve the stationary distribution (distribution of states) of the hybrid attack (or one-time releasing when \rho = 1) which is modeled as a Markov problem. 

### Basic Usage

Run *MarkovChainSolver.py* to solve a stationary distribution for given parameters (alpha, rho). 

The transition matrix is filled with probability values of hybrid attack model.





## Hybrid Attack by Renting Power

The simulation of a mining pool launching a hybrid attack by renting mining power.

### Basic Usage

Run *hybrid_attack_by_renting_power.py* to simulate a mining pool launches a hybrid attack by renting mining power. We set the total hashrate (i.e., mining power) of the Bitcoin network is 133731.55 PH/s (The data is obtained from [Crypto51](https://www.crypto51.app/) at 16:00 on September 13th, 2021), the power fraction owned by pool is 0.1780 (i.e., 17.80%, AntPool's mining power at that time), the rented fraction is 0.0920 (to reach the 27%). 

By default, we let the pool rent mining power for 24 hours, and launch the hybrid attack with parameter \rho=1.0. The simulation is run 100,000 times totally, then the results are averaged. In each simulation, 144 blocks are found on the longest public chain. 

For more details about hybrid attack implementation, see **Hybrid Attack** above.





## Credit to

https://github.com/Luc-Bertin/Selfish-Mining-Simulator

This guy's code is very helpful!

