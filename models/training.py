# Importing the libraries
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

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
        
        # Convert environment values to states 
        state = self.ai_input_provider.calculate_ai_input(self.env_values)
        print('State inputs to Q-Network')
        print(state)
        
        # Update brain
        action = self.brain.update(self.last_reward, state)
        
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
        plt.plot(self.scores, color='red')
        plt.ylabel('Average reward score per epochs')
        plt.xlabel('Training epochs')
        plt.title('Training curves tracking the agent average score')
        plt.savefig(os.path.join(path, str(name) + '.pdf'), format='pdf')