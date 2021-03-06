# Echo server
import time

class StartUp():
    def __init__(self, params, env):
        self.params = params
        self.env = env
        self.T1 = 0
        self.T2 = 0
        self.T3 = 0
        self.T4 = 0
        self.Tmix = 0
        self.Treturn = 0
        self.WhileHolder_1 = True
        self.WhileHolder_2 = True
        self.min = 28
        self.count = 0
        self.stopper = 0
        
    def start_script(self):
        # Set Tmix to max
        self.env.sendAction(30)
        # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
        time.sleep(0.1)
        # Open all valves
        self.env.sendAction(4)
        
        # Up
        while self.WhileHolder_1:
            print('------------------------------------------------')
            print('Start up script is running')
            # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
            time.sleep(0.1)
            #Receive values from Simulink environment
            env_values = self.env.receiveState()
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
               
            # Close valves depending on they have achieved reference temperatures
            if self.T1 > self.params.goalT1 and self.T2 > self.params.goalT2 and self.T3 > self.params.goalT3 and self.T4 > self.params.goalT4:
                if self.stopper == 0 or self.stopper == 2 or self.stopper == 4:
                    self.stopper += 1
                elif self.stopper == 6:
                    exit(1)
                
                self.env.sendAction(19) # Close all valves
                print('Close all valves')
                
            elif self.T1 < self.min and self.T2 < self.min and self.T3 < self.min and self.T4 < self.min:
                self.env.sendAction(4) # Open all valves
                print('Open all valves')
                if self.stopper == 1 or self.stopper == 3 or self.stopper == 5:
                    self.stopper += 1
            else:
                self.env.sendAction(30) # Satisfy timeout in simulink by keep sending data
                
            
