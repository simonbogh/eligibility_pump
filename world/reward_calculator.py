import numpy as np


class RewardCalculator:
    def __init__(self, params):
        self.last_distance = 0
        self.params = params

    def calculate_reward(self, env_values):
        
        # Values from environment
        T1, T2, T3, T4, Tsource = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4]
        
		# Absolute distance from temperatures to goal
        distance = ((abs(self.params.goalT1 - T1)))# + abs(signalT1 - goal_T2) + abs(signalT1 - goal_T3) + abs(signalT1 - goal_T4))/4)
        print('distance is ', distance)
        
		# Reward Policy
        if 0 <= distance <= 0.3:
            last_reward = 1
            if distance < self.last_distance:
            	last_reward -= 0.2
        elif T1 < 16 or T1 > 39:
            last_reward = -1
            if distance < self.last_distance:
            	last_reward = self.last_distance*0.8
        elif distance < self.last_distance:
            last_reward = 0.3
        else:
            last_reward = -0.06*distance

        print('reward is ', last_reward)
        
		#Update
        self.last_distance = distance
        
        return last_reward
