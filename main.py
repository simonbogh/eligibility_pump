# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/

# Import libraries
import argparse
import os
import time

# Importing shared Python files between models
from shared.reward_calculator import RewardCalculator
from shared.env import environment
from shared.ai_input_provider import AiInputProvider

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
parser.add_argument('-model', help='Model type - DQN is with tensorflow and DQN LSTM is pytorch and DQNELI is with tensorflow (DQN is default)', choices=[DQN, DQNLSTM, DQNELI])

args = parser.parse_args()

# Adding this line if we don't want the right click to put a red point
SAVES = "./saves"
SAVES_BRAINS = "%s/brains" % SAVES
SAVES_PLOTS = "%s/plots" % SAVES

# Ensure directory for brain and plots
def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

ensure_dir(SAVES)
ensure_dir(SAVES_BRAINS)
ensure_dir(SAVES_PLOTS)

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
        self.hidden_size = 30
        self.action_size = 3
        # Eligibility trace steps
        self.n_steps = 0
        # Reference
        self.goalT1 = 27
        self.goalT2 = 0
        self.goalT3 = 0
        self.goalT4 = 0
		# Action selector
        self.action_selector = 1 #1 Softmax #2 Epsilon Greedy

# Default parameters
params = Params()

# Chosen parameters
# If not chosen then choose default mentioned in help
params.n_steps = args.en if args.en else 1
params.lr  = args.lr if args.lr else 0.001
params.gamma = args.gamma if args.gamma else 0.9
params.tau = args.tau if args.tau else 50
args.eb = args.eb if args.eb else 'brain'
params.hidden_size = args.hn if args.hn else 30
params.eps_start = args.es if args.es else 0.9
params.eps_end = args.ee if args.ee else 0.1
params.eps_decay = args.ed if args.ed else 2000

if args.acs == EPS:
    params.action_selector = 2
else:
    params.action_selector = 1


########### Run the whole thing ###############

# Create standard obejcts for all models

# Creating Connection for sender and receiver socket
env = environment()
env.createServerSockets()

# Creating calculaters
reward_calculator = RewardCalculator(params)
ai_input_provider = AiInputProvider(params)

# Load specific files and create specific obects for model with respect to platform
# Due to the setup is a bit different when programmed ai in torch and tensorflow the following is needed
if args.model == DQNELI: # Tensorflow specific code eligibility
    # Importing Python files
    from models.eligibility_trace.infra.save_orchestrator import SaveOrchestrator
    from models.eligibility_trace.infra.score_history import ScoreHistory
    from models.eligibility_trace.world.ai import AI
    from models.eligibility_trace.world.updater import Updater
    from models.eligibility_trace.ai.tf.ai_self_tf import Dqn
    # Creating score history
    score_history = ScoreHistory()
    # Creating brain
    ai = AI(params, Dqn)
    # Creating training object
    training = Updater(reward_calculator, ai_input_provider, ai, score_history, env, params)
    # Load brain if requested
    if args.sb:
        save_orchestrator.load_brain(os.path.join(SAVES_BRAINS, args.sb))
    # Create brain module in folder
    save_orchestrator = SaveOrchestrator("saves/", ai.brain)
    
else: # Pytorch specific code DQN and DQN + LSTM
    # Import Python files
    from models.training import Training
    # Create training object
    if args.model == DQNLSTM:
        from models.DRL_Qnetwork_LSTM import DQN_LSTM
        ai = DQN_LSTM(params)
    else:
        from models.DRL_Qnetwork import DQN
        ai = DQN(params)
    # Creating training object
    training = Training(params, ai, env, reward_calculator, ai_input_provider)
    
    # Load brain if requested
    if args.sb:
        ai.load_brain(os.path.abspath(SAVES_BRAINS), args.sb)
    

# Have to send the first communication to Simulink in order to start the simulation
env.sendAction(0)

iter = 0
while True:
    print('------------------------------------------------')
    print('iteration ', iter)
    t0 = time.time()
    
    # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
    time.sleep(0.1)
    
    # Update brain with received environment values and calculate action
    training.update()
    
    if iter % 500 == 0: # Save every 500 times to have less computational
        if args.model == DQNELI:
                # Save brain
                save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.eb))
                # Save brain plot
                score_history.save_brainplot()
        else:
                # Save brain
                ai.save_brain(os.path.abspath(SAVES_BRAINS), args.eb)
                # Save brain plot
                training.save(os.path.abspath(SAVES_PLOTS), args.eb)
        
    
    # Survilance of execution time performance
    t1 = time.time()
    iter += 1
    print('Execution time of iteration ', t1-t0)


