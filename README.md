# AI pump

The objective is that the ai from python select the actions in order to meet a reference temperature set in the python code.
The actions are up in temperature, down in temperature and the third is do nothing. The temperature set by python cannot 
go higher than 40 or lower than 15. The model have no dynamics from a house and is therefore only a test simulation to
see if you algorithm can hit a sudden reference temperature which in this case is 27.
  
# The following libraries are needed to run
* tensorflow or pytorch
* numpy
* matplotlib
  
  
# Parameters to on main.py:  
    -sb -- (sb = Start Brain) - Name of brain to start with, from saves/brains'  
    -eb -- (eb = End Brain) - Name of brain to write to after the iterations are done, from saves/brains' (same name of plot will be in saves/plots)  
    -en -- (en = eligibility trace steps n) - How many steps should eligiblity trace steps take (1 is default, is simple one step Q learning  
    -lr -- (lr = Learning rate) - 0.001 is default  
    -gamma -- (gamma = Discount factor) - 0.9 is default'  
    -tau' -- (tau = Temperature for softmax function) - 50 is default'  
    -hn -- (hd = hidden neurons) - For neural network (30 is default with one hidden layer')  
    -tau -- (tau = Temperature) - For Softmax function (50 is default')  
    -es -- (es = Epsilon start) - For epsilon Greedy start value, meaning random action is taken 90% of the time (0.9 is default')  
    -ee -- (ee = Epsilon end) - For epsilon Greedy end value, meaning random action is taken 10% of the time after decay(0.1 is default')  
    -ed -- (ed = Epsilon decay) - For epsilon Greedy, by default decay from 0.9 to 0.1 over 2000 steps (2000 is default')  
    -acs -- (acs = action selector) - (softmax is default)', choices=[SOFTMAX, EPS])  
    -model -- Model type - DQN is with tensorflow and DQN LSTM is pytorch and DQNELI is with tensorflow (DQN is default)', choices=[DQN, DQNLSTM, DQNELI])  
  
    
Forexample, below the user specific specifies that he/she wants tau = 20, and model should be DQN from pytorch
  
python main.py -tau 20 -model dqn
  
  
TCP connect receiver and send port by running Simulink model <TestModel_3a.slx>. (notice first time starting Simulation can result in 
no connection to TCP/IP server established by python. Simply just run the script again and start the simulation yet again)