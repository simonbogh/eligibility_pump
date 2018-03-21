# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/

# Import libraries
import argparse
import os
import time

# Importing Python files
from models.eligibility_trace.infra.save_orchestrator import SaveOrchestrator
from models.eligibility_trace.infra.score_history import ScoreHistory
from models.eligibility_trace.world.ai import AI
from models.eligibility_trace.world.ai_input_provider import AiInputProvider
from models.eligibility_trace.world.updater import Updater
from models.eligibility_trace.ai.tf.ai_self_tf import Dqn
from shared.reward_calculator import RewardCalculator
from shared.env import environment

# Action Selectors
SOFTMAX, EPS = ("softmax","eps")
# Model Types
DQN, DQNLSTM, DQNELI = ("dqn","dqnlstm", "dqneli")

parser = argparse.ArgumentParser(description='Run Pump AI.')
parser.add_argument('-sb', help='(sb = Start Brain) - Name of brain to start with, from saves/brains')
parser.add_argument('-eb', help='(eb = End Brain) - Name of brain to write to after the iterations are done, from saves/brains')
parser.add_argument('-en', type=int, help='(en = eligibility trace steps n) - How many steps should eligiblity trace take (1 is default, is simple one step Q learning)')
parser.add_argument('-lr', type=int, help='(lr = Learning rate) - (0.001 is default')
parser.add_argument('-gamma', type=int, help='(gamma = Discount factor) - (0.9 is default')
parser.add_argument('-hn', type=int, help='(hd = hidden neurons) - For neural network (30 is default with one hidden layer')
parser.add_argument('-tau', type=int, help='(tau = Temperature) - For Softmax function (50 is default')
parser.add_argument('-es', type=int, help='(es = Epsilon start) - For epsilon Greedy start value, meaning random action is taken 90% of the time (0.9 is default')
parser.add_argument('-ee', type=int, help='(ee = Epsilon end) - For epsilon Greedy end value, meaning random action is taken 10% of the time after decay(0.1 is default')
parser.add_argument('-ed', type=int, help='(ed = Epsilon decay) - For epsilon Greedy, by default decay from 0.9 to 0.1 over 2000 steps (2000 is default')
parser.add_argument('-acs', help='(acs = action selector) - (softmax is default)', choices=[SOFTMAX, EPS])
parser.add_argument('-model', help='Model type - DQN and DQN LSTM is pytorch and DQNELI is with tensorflow (DQN is default)', choices=[DQN, DQNLSTM, DQNELI])

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
		# Parameter of RL
        self.lr = 0.001
        self.gamma = 0.9
        # Softmax
        self.tau = 50
        #Epsilon Greedy
        self.eps_start = 0.9
        self.eps_end = 0.05
        self.eps_decay = 2000
        # Replay Memory
        self.ER_sample_size = 160
        self.ER_batch_size = 300
        self.ER_capacity = 100000
        # Neural Network
        self.input_size = 2
        self.h_neurons = 30
        # Eligibility trace steps
        self.n_steps = 0
        # Reference
        self.goalT1 = 27
        self.goalT2 = 0
        self.goalT3 = 0
        self.goalT4 = 0
		# Action selector
        self.action_selector = 1 #1 Softmax #2 Epsilon Greedy
        # Model Types
        self.model = 1

# Default parameters
params = Params()

# Chosen parameters
# If not chosen then choose default mentioned in help
params.n_steps = args.en if args.en else 1
params.lr  = args.lr if args.lr else 0.001
params.gamma = args.gamma if args.gamma else 0.9
params.tau = args.tau if args.tau else 50
args.eb = args.eb if args.eb else 'brain'
params.h_neurons = args.hn if args.hn else 30
params.eps_start = args.es if args.es else 0.9
params.eps_end = args.ee if args.ee else 0.1
params.eps_decay = args.ed if args.ed else 2000

if args.acs == EPS:
    params.action_selector = 2
else:
    params.action_selector = 1


# Run the whole thing

# Create standard obejcts for all models
# Creating Connection for sender and receiver socket
env = environment()
env.createServerSockets()

# Creating calculaters
reward_calculator = RewardCalculator(params)


# Create object for chosen model
if args.model == DQNELI:
    # Tensorflow specific code eligibility
    # Creating score history
    score_history = ScoreHistory()
    ai_input_provider = AiInputProvider(params)
    # Creating brain
    ai = AI(params, Dqn)
    training = Updater(reward_calculator, ai_input_provider, ai, score_history, env, params)
    if args.sb:
        save_orchestrator.load_brain(os.path.join(SAVES_BRAINS, args.sb))
    # Create brain module in folder
    save_orchestrator = SaveOrchestrator("saves/", ai.brain)
else:
    from models.training import Training
    
    # Create training object
    training = Training(params)
    
    # Load experience replay (brain)
    #training = Training(params)
    
    if args.model == DQNLSTM:
        print('hej so')
    else: #DQN
        print('hej')


# Have to send the first communication to Simulink in order to start the simulation
env.sendAction(0)

iter = 0
while True:
    print('------------------------------------------------')
    print('iteration ', iter)
    t0 = time.time()
    
    # Sleep in order to make sure Simulink and Python can have a good TCP/IP communication
    time.sleep(0.1)
    
    if args.model == DQNELI:
        # Update brain
        training.update()
        # Save brain file and plot
        if iter % 500 == 0:
            save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.eb))
            score_history.save_brainplot()
    else:
        # Update brain
        training.update()
		# Save brain and score (+ print score plot to working directory)
        if iter % 500 == 0: # Save every 500 times to have less computational
            training.save()
    
    
    t1 = time.time()
    iter += 1
    print('Full execution time ', t1-t0)


