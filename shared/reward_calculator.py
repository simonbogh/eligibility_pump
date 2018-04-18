import numpy as np


class RewardCalculator:
    def __init__(self, params):
        self.last_distance1 = 0
        self.last_distance2 = 0
        self.last_distance3 = 0
        self.last_distance4 = 0
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tmix = 0
        self.Treturn = 0
        self.count = 0

        
    def calculate_reward(self, env_values, Cn_valves):
        
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
        distance1 = abs(self.params.goalT1 - T1)
        distance2 = abs(self.params.goalT2 - T2)
        distance3 = abs(self.params.goalT3 - T3)
        distance4 = abs(self.params.goalT4 - T4)
        print('distance1 is ', distance1)
        print('distance2 is ', distance2)
        print('distance3 is ', distance3)
        print('distance4 is ', distance4)
        
        max_dist = 0.5
        
		# Reward Policy - Circuit 1
        if 0 <= distance1 <= max_dist and Cn_valves.C1_valve:
            last_reward1 = 1
            if distance1 < self.last_distance1:
                last_reward1 = last_reward1* (1 - distance1)
        elif 0 <= distance1 <= max_dist:
            last_reward1 = 0.5
            if distance1 < self.last_distance1:
                last_reward1 = last_reward1* (1 - distance1)
        elif distance1 < self.last_distance1:
            last_reward1 = 0.1
        elif T1 < 15.1 or T1 > 29.9 or Tmix < 15.1 or Tmix > 44.9:
            last_reward1 = -1
        else:
            last_reward1 = -0.1*distance1
            
            
		# Reward Policy - Circuit 2
        if 0 <= distance2 <= max_dist and Cn_valves.C2_valve:
            last_reward2 = 1
            if distance2 < self.last_distance2:
                last_reward2 = last_reward2* (1 - distance2)
        elif 0 <= distance2 <= max_dist:
            last_reward2 = 0.5
            if distance2 < self.last_distance2:
                last_reward2 = last_reward2* (1 - distance2)
        elif distance2 < self.last_distance2:
            last_reward2 = 0.1
        elif T2 < 15.1 or T2 > 29.9 or Tmix < 15.1 or Tmix > 44.9:
            last_reward2 = -1
        else:
            last_reward2 = -0.1*distance2
            
            
		# Reward Policy - Circuit 3
        if 0 <= distance3 <= max_dist and Cn_valves.C3_valve:
            last_reward3 = 1
            if distance3 < self.last_distance3:
                last_reward3 = last_reward3* (1 - distance3)
        elif 0 <= distance3 <= max_dist:
            last_reward3 = 0.5
            if distance3 < self.last_distance3:
                last_reward3 = last_reward3* (1 - distance3)
        elif distance3 < self.last_distance3:
            last_reward3 = 0.1
        elif T3 < 15.1 or T3 > 29.9 or Tmix < 15.1 or Tmix > 44.9:
            last_reward3 = -1
        else:
            last_reward3 = -0.1*distance3
            
            
		# Reward Policy - Circuit 4
        if 0 <= distance4 <= max_dist and Cn_valves.C4_valve:
            last_reward4 = 1
            if distance4 < self.last_distance4:
                last_reward4 = last_reward4* (1 - distance4)
        elif 0 <= distance4 <= max_dist:
            last_reward4 = 0.5
            if distance4 < self.last_distance4:
                last_reward4 = last_reward4* (1 - distance4)
        elif distance4 < self.last_distance4:
            last_reward4 = 0.1
        elif T4 < 15.1 or T4 > 29.9 or Tmix < 15.1 or Tmix > 44.9:
            last_reward4 = -1
        else:
            last_reward4 = -0.1*distance4
            
        #Update
        self.last_distance1 = distance1
        self.last_distance2 = distance2
        self.last_distance3 = distance3
        self.last_distance4 = distance4
        
        # Sum rewards and divide by number of circuits
        last_reward = (last_reward1 + last_reward2 + last_reward3 + last_reward4) / 4

        
        return last_reward
