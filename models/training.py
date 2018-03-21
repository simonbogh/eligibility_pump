# Importing the libraries
import matplotlib.pyplot as plt

# importing the brain
from models.DRL_Qnetwork import DQN
from models.DRL_Qnetwork_LSTM import DQN_LSTM


# Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
last_reward = 0 # updates reward
scores = [] # contain some of the sum of rewards
# Initializing the last distance from temp ref to temp goal
last_distance = 0

# Creating the
class Training():
	def __init__(self, params):
		if params.model is 1: #Q network
			self.brain = DQN(params)
		elif params.model is 2: #Q network with LSTM
			self.brain = DQN_LSTM(params)
			
		self.goalT1 = params.goalT1
		self.goalT2 = params.goalT1
		self.goalT3 = params.goalT1
		self.goalT4 = params.goalT1
        
		self.steps_since_last_goal = 0

	def update(self, signalT1, Tsource):#, signalT2, signalT3, signalT4):
		global action
		global last_reward
		global last_distance
		scores
		
        # Normalize input data
		signalT1_norm = (signalT1-15)/25
		orientation = (signalT1-self.goalT1)/12.5
		Tsource_norm = (Tsource - 15)/25
        # Input vector to NN
		last_signal = [signalT1_norm, orientation]
		print('last_signal is ', last_signal)
        # Output vector from NN - select action to accomplish goal
		self.action = self.brain.update(last_reward, last_signal)
		#update score
		scores.append(self.brain.score())
		# Absolute distance from temperatures to goal
		distance = ((abs(self.goalT1 - signalT1)))# + abs(signalT1 - goal_T2) + abs(signalT1 - goal_T3) + abs(signalT1 - goal_T4))/4)
		print('distance is ', distance)
        
		# Reward Policy
		if 0 <= distance <= 0.3:
			last_reward = 1
			if distance < last_distance:
				last_reward -= 0.2
		elif signalT1 < 16 or signalT1 > 39:
			last_reward = -1
			if distance < last_distance:
				last_reward = last_distance*0.8
		elif distance < last_distance:
			last_reward = 0.3
		else:
			last_reward = -0.06*distance

            
		print('reward is ', last_reward)
		
        #Update
		last_distance = distance    
        
    
	def actionFromNN(self):
		return self.action
	
	def getScores(self):
		return scores
		
	# Saving experience
	def save(self):
		self.brain.save()
		plt.plot(scores)
		plt.ylabel('Average reward score per epochs')
		plt.xlabel('Training epochs')
		plt.title('Training curves tracking the agent average score')
		plt.savefig('Brain_plot.png')
		
	# Loading experience
	def load(self):
		print("loading last saved brain...")
		self.brain.load()