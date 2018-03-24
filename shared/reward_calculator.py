import numpy as np


class RewardCalculator:
    def __init__(self, params):
        self.last_distance = 0
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tsource = 0
        
    def calculate_reward(self, env_values):
        
        # Try, do to that simulink sometimes sends empty arrays
        # This can happen every 2000 or 15000 times
        try:
            # Values from environment
            T1, T2, T3, T4, Tsource = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4]
            self.T1, self.T2, self.T3, self.T4, self.Tsource = T1, T2, T3, T4, Tsource
            print('Enrionment Values are [T1,T2,T3,T4,Tsource]')
            print('Enrionment Values are [', T1,',', T2,',', T3,',', T4,',', Tsource,']')
        except:
           T1, T2, T3, T4, Tsource = self.T1, self.T2, self.T3, self.T4, self.Tsource
           

		# Absolute distance from temperatures to goal
        distance = ((abs(self.params.goalT1 - T1)))
        print('distance is ', distance)
        
		# Reward Policy
        if 0 <= distance <= 0.3:
            last_reward = 1
            if distance < self.last_distance:
            	last_reward -= 0.3*distance
        elif T1 < 16 or T1 > 39:
            last_reward = -1
            if distance < self.last_distance:
            	last_reward = last_reward*0.8
        elif distance < self.last_distance:
            last_reward = 0.3
        else:
            last_reward = -0.06*distance
        
		#Update
        self.last_distance = distance
        
        return last_reward
