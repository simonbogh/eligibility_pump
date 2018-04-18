
class AiInputProvider:
    def __init__(self, params):
        #self.normalizer = normalizer
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tmix = 0
        self.Treturn = 0
        self.last_T1 = 0
        self.last_T2 = 0
        self.last_T3 = 0
        self.last_T4 = 0
        self.C1_valve = 0
        self.C2_valve = 0
        self.C3_valve = 0
        self.C4_valve = 0
        
    def calculate_ai_input(self, env_values, action):
        
        # Try, do to that simulink sometimes sends empty arrays
        # This can happen every 2000 or 15000 times
        try:
            # Values from environment
            T1, T2, T3, T4, Tmix, Treturn = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4], env_values[5]
            self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn = T1, T2, T3, T4, Tmix, Treturn
        except:
           T1, T2, T3, T4, Tmix, Treturn = self.T1, self.T2, self.T3, self.T4, self.Tmix, self.Treturn
        
        # Standadize input data
        # Orientation
        if (T1-self.params.goalT1) <= 0:
            orientation1_std = 0.5
        else:
            orientation1_std = -0.5

        if (T2-self.params.goalT2) <= 0:
            orientation2_std = 0.5
        else:
            orientation2_std = -0.5
            
        if (T3-self.params.goalT3) <= 0:
            orientation3_std = 0.5
        else:
            orientation3_std = -0.5

        if (T4-self.params.goalT4) <= 0:
            orientation4_std = 0.5
        else:
            orientation4_std = -0.5
            
        # Room Temperature
        T1_std = (T1 ) / 35
        T2_std = (T2 ) / 35
        T3_std = (T3 ) / 35
        T4_std = (T4 ) / 35
        
        # Diff
        diff1_std = abs((T1 - self.last_T1)* 10)
        diff2_std = abs((T2 - self.last_T2)* 10)
        diff3_std = abs((T3 - self.last_T3)* 10)
        diff4_std = abs((T4 - self.last_T4)* 10)
        
        # Mix and return temperature
        Tmix_std = (Tmix - 15)/30
        Treturn_std = (Treturn - 10)/ 25
        
        # Update
        self.last_T1 = T1
        self.last_T2 = T2
        self.last_T3 = T3
        self.last_T4 = T4
        
        # Circuit valves open or close ?
        if action ==  4:
            self.C1_valve = 1
            self.C2_valve = 1
            self.C3_valve = 1
            self.C4_valve = 1
        elif action ==  5:
            self.C1_valve = 1
            self.C2_valve = 0
            self.C3_valve = 0
            self.C4_valve = 0
        elif action ==  6:
            self.C1_valve = 0
            self.C2_valve = 1
            self.C3_valve = 0
            self.C4_valve = 0
        elif action ==  7:
            self.C1_valve = 0
            self.C2_valve = 0
            self.C3_valve = 1
            self.C4_valve = 0
        elif action ==  8:
            self.C1_valve = 0
            self.C2_valve = 0
            self.C3_valve = 0
            self.C4_valve = 1
        elif action ==  9:
            self.C1_valve = 1
            self.C2_valve = 1
            self.C3_valve = 0
            self.C4_valve = 0
        elif action ==  10:
            self.C1_valve = 0
            self.C2_valve = 1
            self.C3_valve = 1
            self.C4_valve = 0
        elif action ==  11:
            self.C1_valve = 0
            self.C2_valve = 0
            self.C3_valve = 1
            self.C4_valve = 1
        elif action ==  12:
            self.C1_valve = 1
            self.C2_valve = 0
            self.C3_valve = 0
            self.C4_valve = 1
        elif action ==  13:
            self.C1_valve = 1
            self.C2_valve = 0
            self.C3_valve = 1
            self.C4_valve = 0
        elif action ==  14:
            self.C1_valve = 0
            self.C2_valve = 1
            self.C3_valve = 0
            self.C4_valve = 1
        elif action ==  15:
            self.C1_valve = 1
            self.C2_valve = 1
            self.C3_valve = 1
            self.C4_valve = 0
        elif action ==  16:
            self.C1_valve = 1
            self.C2_valve = 1
            self.C3_valve = 0
            self.C4_valve = 1
        elif action ==  17:
            self.C1_valve = 1
            self.C2_valve = 0
            self.C3_valve = 1
            self.C4_valve = 1
        elif action ==  18:
            self.C1_valve = 0
            self.C2_valve = 1
            self.C3_valve = 1
            self.C4_valve = 1
        elif action ==  19:
            self.C1_valve = 0
            self.C2_valve = 0
            self.C3_valve = 0
            self.C4_valve = 0
        
        orientation1 = (T1-self.params.goalT1)
        orientation2 = (T2-self.params.goalT2)
        orientation3 = (T3-self.params.goalT3)
        orientation4 = (T4-self.params.goalT4)
        
        diff1 = abs(T1 - self.last_T1)
        diff2 = abs(T2 - self.last_T2)
        diff3 = abs(T3 - self.last_T3)
        diff4 = abs(T4 - self.last_T4)
        
        # Standadize
        state =  [T1_std, orientation1_std, diff1_std, self.C1_valve, T2_std, orientation2_std, diff2_std, self.C2_valve, T3_std, orientation3_std, diff3_std, self.C3_valve, T4_std, orientation4_std, diff4_std, self.C4_valve, Tmix_std]
        
        # Normalize
        #state =  [T1, orientation1, diff1, self.C1_valve, T2, orientation2, diff2, self.C2_valve, T3, orientation3, diff3, self.C3_valve, T4, orientation4, diff4, self.C4_valve, Tmix]
        #self.normalizer.observe(state)
        #state = normalizer.normalize(state)
        #state[3] = self.C1_valve
        #state[7] = self.C2_valve
        #state[11] = self.C3_valve
        #state[15] = self.C4_valve
        
        
        return state
        