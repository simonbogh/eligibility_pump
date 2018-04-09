# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/

# Import libraries
import argparse
import os
import time

# Importing shared Python files between models
from shared.reward_calculator import RewardCalculator
from shared.env import environment
from shared.ai_input_provider import AiInputProvider
from shared.parameters import Params

# For yes and no options
YES, NO = ("yes", "no")
# Action Selectors
SOFTMAX, EPS = ("softmax","eps")
# Model Types
TORCH_DQN, TORCH_DQNLSTM, TORCH_DQNET, TF_DQNET = ("torch_dqn","torch_dqnlstm", "torch_dqnet", "tf_dqnet")

parser = argparse.ArgumentParser(prog='Pump AI')
# Optional
parser.add_argument('-sb', help='(Start Brain) - Name of brain to start with, from saves/brains')
parser.add_argument('-eb', help='(End Brain) - Name of brain which is saved in saves/brains and name of brain plot which is saved in saves/plots (default brain)')
parser.add_argument('-ers', help='(experience replay sample size) - how much to sample when learning, Note: only for tf_dqnet (160 is default)')
parser.add_argument('-erb', help='(experience replaybatch size) - how much to use when learning (default 300)')
parser.add_argument('-erc', help='(experience replay capacity) - size of experience replay memory (default 100000)')
parser.add_argument('-lr', type=int, help='(Learning rate) - (0.001 is default')
parser.add_argument('-gamma', type=int, help='(Discount factor) - (0.9 is default')
parser.add_argument('-tau', type=int, help='(Temperature) - For Softmax function, note: when choosing torch_dqnet tau should be 1-10 (50 is default')
parser.add_argument('-es', type=int, help='(Epsilon start) - For epsilon Greedy start value, meaning random action is taken 90%% of the time (0.9 is default)')
parser.add_argument('-ee', type=int, help='(Epsilon end) - For epsilon Greedy end value, meaning random action is taken 5%% of the time after decay(0.05 is default)')
parser.add_argument('-ed', type=int, help='(Epsilon decay) - For epsilon Greedy, by default decay from 0.9 to 0.1 over 2000 steps (2000 is default')
parser.add_argument('-acs', help='(action selector) - (softmax is default) Note: epsilon greedy is not made for eligibility trace', choices=[SOFTMAX, EPS])
parser.add_argument('-en', type=int, help='(eligibility trace steps n) - How many steps should eligiblity trace take (1 is default, is simple one step Q learning)')
parser.add_argument('-ins', help='(input size) - number of input variables to q-network (default 2)')
parser.add_argument('-hn', type=int, help='(hidden neurons) - For neural network (30 is default with one hidden layer')
parser.add_argument('-asize', help='(action size) - number of out variables from q-network (default 2)')
parser.add_argument('-t1', help='Reference temperature in circuit 1 (default 22)')
parser.add_argument('-t2', help='Reference temperature in circuit 2 (default 22)')
parser.add_argument('-t3', help='Reference temperature in circuit 3 (default 22)')
parser.add_argument('-t4', help='Reference temperature in circuit 4 (default 22)')
parser.add_argument('-lm', help='(Learning Mode) - Q-network will be updated if active (Learning mode is active by default)', choices=[NO])
parser.add_argument('-startup', help=' This set environment to optimal state before proceeding with DRL algorithm (No, not active by default)', choices=[YES])

# Required
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-model', help='torch_dqn, torch_dqnlstm, torch_dqnet is in pytorch and tf_dqnet is in tensorflow (dqn = deep q-network, eli = eligibility_trace)', choices=[TORCH_DQN, TORCH_DQNLSTM, TORCH_DQNET, TF_DQNET], required=True)



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

# Default parameters
params = Params()

# Chosen parameters
# If not chosen then choose default mentioned in help
# Parameter of RL
params.lr  = args.lr if args.lr else 0.001
params.gamma = args.gamma if args.gamma else 0.9
#Softmax
params.tau = args.tau if args.tau else 100
#Epsilon Greedy
params.eps_start = args.es if args.es else 0.9
params.eps_end = args.ee if args.ee else 0.05
params.eps_decay = args.ed if args.ed else 2000
#Experience replay memory
params.ER_sample_size = args.ers if args.ers else 160
params.ER_batch_size = args.erb if args.erb else 300
params.ER_capacity = args.ec if args.erb else 100000
#Qnetwork
params.input_size = args.ins if args.ins else 9
params.hidden_size = args.hn if args.hn else 30
params.action_size = args.asize if args.asize else 7
#Eligibility trace
params.n_steps = args.en if args.en else 1
# Reference
params.goalT1 = args.t1 if args.t1 else 22
params.goalT2 = args.t2 if args.t2 else 22
params.goalT3 = args.t3 if args.t3 else 22
params.goalT4 = args.t4 if args.t4 else 22
#Name of brain
args.eb = args.eb if args.eb else 'brain'
if args.acs == EPS:
    params.action_selector = 2
else:
    params.action_selector = 1
#learning mode
if args.lm == NO:
    params.learning_mode = 0
else:
    params.learning_mode = 1

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
if args.model == TF_DQNET: # Tensorflow specific code eligibility
    # Importing Python files
    from models.eligibility_trace_tf.infra.save_orchestrator import SaveOrchestrator
    from models.eligibility_trace_tf.infra.score_history import ScoreHistory
    from models.eligibility_trace_tf.world.ai import AI
    from models.eligibility_trace_tf.world.updater import Updater
    from models.eligibility_trace_tf.ai.tf.ai_self_tf import Dqn
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
    
elif args.model == TORCH_DQN or args.model == TORCH_DQNLSTM: 
    # Pytorch specific code DQN and DQN + LSTM
    # Import Python files
    from models.training import Training

    if args.model == TORCH_DQNLSTM:
        from models.DRL_Qnetwork_LSTM import DQN_LSTM
        # Create ai
        ai = DQN_LSTM(params)
    else:
        from models.DRL_Qnetwork import DQN
        # Create ai
        ai = DQN(params)
        
    # Creating training object
    training = Training(params, ai, env, reward_calculator, ai_input_provider)
    
    # Load brain if requested
    if args.sb:
        ai.load_brain(os.path.abspath(SAVES_BRAINS), args.sb)
        
elif args.model == TORCH_DQNET:
    #Importing Python Files
    from models.DRL_Qnetwork import Network
    from models.eligibility_trace_torch.ai import SoftmaxBody, AI, Training
    from models.eligibility_trace_torch.experience_replay_eligibility import NStepProgress, ReplayMemory
    
    # Create network
    dqn = Network(params)
    # Create softmax body
    softmax_body = SoftmaxBody(params.tau)
    # Create ai
    ai = AI(dqn, softmax_body)
    
    # Setting up Experience Replay for eligibility trace
    n_steps = NStepProgress(env, ai, params.n_steps, reward_calculator, ai_input_provider)
    eligibility_memory = ReplayMemory(n_steps, params.ER_capacity)
    
    # Create training object
    training = Training(params, ai, eligibility_memory, n_steps, dqn)

    # Load brain if requested
    if args.sb:
        training.load_brain(os.path.abspath(SAVES_BRAINS), args.sb)
    

# Have to send the first communication to Simulink in order to start the simulation
env.sendAction(0)

# Start up script inorder to set environment to same position as when we stopped learning
# This is done because the experience replay does not know how to deal with these "new"
# states because we delete those from the beginning
if args.startup == YES:
    from shared.startup_script import StartUp
    startup_script = StartUp(params, env)
    startup_script.start_script()

iter = 0
while True:
    print('------------------------------------------------')
    print('iteration ', iter)
    t0 = time.time()
    
    # Update brain with received environment values and calculate action
    training.update()
    
    if iter % 500 == 0: # Save every 500 times to have less computational
        if args.model == TF_DQNET:
            # Save brain
            save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.eb))
            # Save brain plot
            score_history.save_brainplot(os.path.abspath(SAVES_PLOTS), args.eb)
        elif args.model == TORCH_DQN or args.model == TORCH_DQNLSTM:
            # Save brain
            ai.save_brain(os.path.abspath(SAVES_BRAINS), args.eb)
            # Save brain plot
            training.save(os.path.abspath(SAVES_PLOTS), args.eb)
        else:
            # Save brain
            training.save_brain(os.path.abspath(SAVES_BRAINS), args.eb)
            # Save brain plot
            training.save_plot(os.path.abspath(SAVES_PLOTS), args.eb)
    
    # Survilance of execution time performance
    t1 = time.time()
    iter += 1
    print('Execution time of iteration ', t1-t0)


