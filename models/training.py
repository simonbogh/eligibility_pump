# Importing the libraries
import matplotlib.pyplot as plt
import os

# Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
#last_reward = 0 # updates reward
#scores = [] # contain some of the sum of rewards

# Creating the
class Training():
    def __init__(self, params, model_type, env, reward_calculator, ai_input_provider):
        self.brain = model_type
        self.env = env
        self.env_values = []
        self.reward_calculator = reward_calculator
        self.ai_input_provider = ai_input_provider
        self.last_reward = 0
        self.scores = []

    def update(self):
        #Receive values from Simulink environment
        self.env_values = self.env.receiveState()
        print('Enrionment Values are [T1,T2,T3,T4,Tsource]')
        print('Enrionment Values are ', self.env_values)
        
        # Convert environment values to states 
        state = self.ai_input_provider.calculate_ai_input(self.env_values)
        
        # Update brain
        action = self.brain.update(self.last_reward, state)
        
        # Get action
        
        
        # Send action to agent in environment
        self.env.sendAction(action + 1)
        print('action is ', action + 1)
        
        # Calculate reward from environment values
        self.last_reward = self.reward_calculator.calculate_reward(self.env_values)
        print('reward is ', self.last_reward)
        
        #update score
        self.scores.append(self.brain.score())
        
    
    def actionFromNN(self):
        return self.action
	
    def getScores(self):
        return scores
		
	# Saving experience
    def save(self, path, name):
        plt.plot(self.scores)
        plt.ylabel('Average reward score per epochs')
        plt.xlabel('Training epochs')
        plt.title('Training curves tracking the agent average score')
        plt.savefig(os.path.join(path, str(name) + '.png'))
		
	# Loading experience
    def load(self):
        print("loading last saved brain...")
        self.brain.load()