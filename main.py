# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/
# Self Driving Car

# Import libraries
import argparse
import os
import time

# Importing Python files
from infra.save_orchestrator import SaveOrchestrator
from infra.score_history import ScoreHistory
from world.ai import AI
from world.ai_input_provider import AiInputProvider
from world.updater import Updater
from world.reward_calculator import RewardCalculator
from world.env import environment
from ai.tf.ai_self_tf import Dqn

parser = argparse.ArgumentParser(description='Run Pump AI.')
parser.add_argument('-sb', help='(sb = Start Brain) - Name of brain to start with, from saves/brains')
parser.add_argument('-eb', help='(eb = End Brain) - Name of brain to write to after the iterations are done, from saves/brains')
parser.add_argument('-en', type=int, help='(en = eligibility trace steps n) - How many steps should eligiblity trace take (1 is default, is simple one step Q learning)')
parser.add_argument('-lr', type=int, help='(lr = Learning rate) - (0.001 is default')
parser.add_argument('-gamma', type=int, help='(gamma = Discount factor) - (0.9 is default')
parser.add_argument('-tau', type=int, help='(tau = Temperature) - (50 is default')


args = parser.parse_args()

# Adding this line if we don't want the right click to put a red point
SAVES = "./saves"
SAVES_BRAINS = "%s/brains" % SAVES

def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

ensure_dir(SAVES)
ensure_dir(SAVES_BRAINS)

# Gathering all the parameters (that we can modify to explore)
class Params():
    def __init__(self):
		# Parameter of algorithm
        self.lr = 0
        self.gamma = 0
        self.tau = 0
        self.ER_sample_size = 160
        self.ER_batch_size = 300
        self.ER_capacity = 100000
        self.input_size = 2
        self.h_neurons = 30
        self.n_steps = 0
        self.goalT1 = 27
        self.goalT2 = 0
        self.goalT3 = 0
        self.goalT4 = 0


# Running the whole thing

# Creating Connection for sender and receiver socket
env = environment()
env.createServerSockets()

# Default parameters
params = Params()

# Chosen parameters
params.n_steps = args.en if args.en else 1
params.lr  = args.lr if args.lr else 0.001
params.gamma = args.gamma if args.gamma else 0.9
params.tau = args.tau if args.tau else 50


# Creating score history
score_history = ScoreHistory()

# Creating calculaters
reward_calculator = RewardCalculator(params)
ai_input_provider = AiInputProvider(params)

# Creating brain
ai = AI(params, Dqn)

# Create brain module in folder
save_orchestrator = SaveOrchestrator("saves/", ai.brain)


training = Updater(reward_calculator, ai_input_provider, ai, score_history, env, params)

if args.sb:
    save_orchestrator.load_brain(os.path.join(SAVES_BRAINS, args.sb))

iter = 0

# Have to send the first communication to Simulink in order to start the simulation
env.sendAction(0)


while True:
    print('------------------------------------------------')
    print('iteration ', iter)
    t0 = time.time()
    
    # Sleep in order to make sure Simulink and Python can have a good TCP/IP communication
    time.sleep(0.1)
    
    # Update brain
    training.update()
    
	# Save brain file and plot
    if iter % 500 == 0:
        save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.eb))
        score_history.save_brainplot()
    
    t1 = time.time()
    iter += 1
    print('Full execution time ', t1-t0)


