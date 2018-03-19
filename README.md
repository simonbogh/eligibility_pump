# AI pump

The objective is that the ai from python select the actions in order to meet a reference temperature set in the python code.
The actions are up in temperature, down in temperature and the third is do nothing. The temperature set by python cannot 
go higher than 40 or lower than 15. The model have no dynamics from a house and is therefore only a test simulation to
see if you algorithm can hit a sudden reference temperature which in this case is 27.

# The following libraries are needed to run
* tensorflow or keras
* numpy
* matplotlib


Parameters to on main.py:
    -im -- (im = implement) - Select implementation to run
    -sb -- (sb = Start Brain) - Name of brain to start with, from saves/brains')
    -eb -- (eb = End Brain) - Name of brain to write to after the iterations are done, from saves/brains')
    -en -- (en = eligibility trace steps n) - How many steps should eligiblity trace steps take (1 is default, is simple one step Q learning)
    
Forexample, here tensorflow (the currently only ai running) where the end brain
that will be saved will be called brainski. Further more is the eligibility
trace set to 10

python main.py -im tf -eb brainski -en 10


TCP connect receiver and send port by running Simulink model <TestModel_3a.slx>. (notice first time starting Simulation can result in 
no connection to TCP/IP server established by python. Simply just run the script again and start the simulation yet again)