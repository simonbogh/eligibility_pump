
class AiInputProvider:
    def __init__(self, params):
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tmix = 0
        self.Treturn = 0
        self.last_T1 = 0
        
    def calculate_ai_input(self, env_values):
        
        # Try, do to that simulink sometimes sends empty arrays
        # This can happen every 2000 or 15000 times
        try:
            # Values from environment
            T1, T2, T3, T4, Tmix, Treturn = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4], env_values[5]
            self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn = T1, T2, T3, T4, Tmix, Treturn
        except:
           T1, T2, T3, T4, Tmix, Treturn = self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn
        
        # Standadize input data
        if (T1-self.params.goalT1) <= 0:
            orientation_std = 0.5
        else:
            orientation_std = -0.5

        T1_std = (T1 - 15)/20
        diff_std = abs((T1 - self.last_T1)* 100)
        Tmix_std = (Tmix - 15)/20
        Treturn_std = (T1 - 15)/20
        
        # Update
        self.last_T1 = T1
        
        return [T1_std, orientation_std, diff_std]#, Treturn_std]#, Tmix_std, Treturn_std]
