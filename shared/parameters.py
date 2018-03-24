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
        self.goalT1 = 22
        self.goalT2 = 22
        self.goalT3 = 22
        self.goalT4 = 22
		# Action selector
        self.action_selector = 1 #1 Softmax #2 Epsilon Greedy