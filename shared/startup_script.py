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
        self.WhileHolder = True
        
    def start_script(self):
        # Set Tmix to max
        self.env.sendAction(30)
        # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
        time.sleep(0.1)
        # Open all valves
        self.env.sendAction(4)
        
        while self.WhileHolder:
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
            if self.T1 > self.params.goalT1 and self.T2 > self.params.goalT2:
                self.env.sendAction(7) # Close both valves
                self.WhileHolder = False
            elif self.T1 > self.params.goalT1:
                self.env.sendAction(6) # Close valve 1 and open valve 2
            elif self.T2 > self.params.goalT2:
                self.env.sendAction(5) # Close valve 2 and open valve 1
            else:
                self.env.sendAction(30) # Satisfy timeout in simulink by keep sending data
                
        # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
        time.sleep(0.1)
        # set Tmix to 35 degrees
        self.env.sendAction(35)
                