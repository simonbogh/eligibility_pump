
class AiInputProvider:
    def __init__(self, params):
        self.params = params
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tsource = 0

    def calculate_ai_input(self, env_values):
        
        # Try, do to that simulink sometimes sends empty arrays
        # This can happen every 2000 or 15000 times
        try:
            # Values from environment
            T1, T2, T3, T4, Tsource = env_values[0], env_values[1], env_values[2], env_values[3], env_values[4]
            self.T1, self.T2, self.T3, self.T4, self.Tsource = T1, T2, T3, T4, Tsource
        except:
           T1, T2, T3, T4, Tsource = self.T1, self.T2, self.T3, self.T4, self.Tsource
        
        # Normalize input data
        T1_norm = (T1-15)/25
        orientation_norm = (T1-self.params.goalT1)/12.5
        Tsource_norm = (Tsource - 15)/25
        
        return [T1_norm, orientation_norm]
