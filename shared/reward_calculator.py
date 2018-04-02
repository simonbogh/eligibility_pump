import numpy as np


class RewardCalculator:
    def __init__(self, params):
        self.last_distance = 0
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tmix = 0
        self.Treturn = 0
        self.count = 0

        
    def calculate_reward(self, env_values):
        
        # Try, do to that simulink sometimes sends empty arrays
        # This can happen every 2000 or 15000 times
        try:
            # Values from environment
            T1, T2, T3, T4, Tmix, Treturn = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4], env_values[5]
            self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn = T1, T2, T3, T4, Tmix, Treturn
            print('Enrionment Values are [ T1 , T2 , T3 , T4 , Tmix, Treturn ]')
            print('Enrionment Values are [', T1,',', T2,',', T3,',', T4,',', Tmix,',', Treturn,']')
        except:
           T1, T2, T3, T4, Tmix, Treturn = self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn
           self.count += 1
           
        print('except  called ', self.count)
		# Absolute distance from temperatures to goal
        distance = abs(self.params.goalT1 - T1)
        print('distance is ', distance)
        
		# Reward Policy
        if 0 <= distance <= 0.5:
            last_reward = 1
            if distance < self.last_distance:
                last_reward = last_reward*distance
        elif distance < self.last_distance:
            last_reward = 0.1
        elif T1 > 29.9 or T1 < 15.1:# or Tmix > 44.9 or Tmix < 15.1:
            last_reward = -1
        else:
            last_reward = -0.1*distance
		#Update
        self.last_distance = distance

        
        return last_reward
