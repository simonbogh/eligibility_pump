from collections import deque

from world.memory.n_step_replay_memory import NStepReplayMemory, Transition, NStepTransition


class Updater:
    def __init__(self, reward_calculator, ai_input_provider, ai, score_history, env, params):
        self.params = params
        self.env = env
        self.score_history = score_history
        self.ai = ai
        self.ai_input_provider = ai_input_provider
        self.reward_calculator = reward_calculator
        self.memory = NStepReplayMemory(params.ER_capacity, params.n_steps)
        self.last_transitions = deque()
        self.step = 0
        self.state = []
        self.env_values = []

    def update(self):
        
        # Convert environment values to state inputs
        if self.step == 0: #In order not to have to much communication
            #Receive values from Simulink environment
            self.env_values = self.env.receiveState()
            
            self.state = self.ai_input_provider.calculate_ai_input(self.env_values)
            self.step += 1
        
        print('Enrionment Values are ', self.env_values)
        # Select action
        action = self.ai.get_next_action(self.state)
        print ('action is ', action)
        
        # Send action to environment
        self.env.sendAction(action)
        
        # Calculate reward from environment values
        reward = self.reward_calculator.calculate_reward(self.env_values)
        print('reward is ', reward)
         
        # save to memory
        self.ai.brain.append_reward(reward)
        self.score_history.append(self.ai.score())
        
        # Receive new state from Simulink Environment
        self.env_values = self.env.receiveState()
        
        # Convert environment values to state inputs
        self.env_values = self.env.receiveState()
        next_state = self.ai_input_provider.calculate_ai_input(self.env_values)
        self.last_transitions.append(Transition(self.state, action, reward, next_state))
		# Update
        self.state = next_state
		

        if len(self.last_transitions) == self.params.n_steps:
            n_step_transition = NStepTransition(self.last_transitions)
            self.memory.push(n_step_transition)
            if len(self.memory.memory) > self.params.ER_batch_size:
                transition_samples = self.memory.sample(self.params.ER_sample_size)
                self.ai.brain.learn_from_transitions(transition_samples)
            self.last_transitions = deque()
