# Experience Replay for eligibility trace in pytorch

# Importing the libraries
import numpy as np
from collections import namedtuple, deque
import time
import pickle
import os

# Defining one Step
Step = namedtuple('Step', ['state', 'action', 'reward'])

# Making the AI progress on several (n_step) steps
class NStepProgress:
    
    def __init__(self, env, ai, n_step, reward_calculator, ai_input_provider):
        self.ai = ai
        self.rewards = []
        self.env = env
        self.n_step = n_step
        self.reward_calculator = reward_calculator
        self.ai_input_provider = ai_input_provider
        self.rewardski = 0
        self.action = 0
    
    def __iter__(self):
        env_values = self.env.receiveState()
        state = self.ai_input_provider.calculate_ai_input(env_values, self.action)
        history = deque()
        reward = 0.0
        while True:
            # Sleep in order to make sure Simulink and Python can have a solid TCP/IP communication
            time.sleep(0.1)
            print('State inputs to brain')
            print(state)
            action = self.ai(np.array([state]))[0][0] # due to it start from 0
            self.env.sendAction(action + 1)
            print('action is', action + 1)
            # Gamle step
            env_values = self.env.receiveState()
            next_state = self.ai_input_provider.calculate_ai_input(env_values, action + 1)
            r = self.reward_calculator.calculate_reward(env_values, self.ai_input_provider)
            print('reward is', r)
            reward += r
            self.rewardski = r
            history.append(Step(state = state, action = action, reward = r))
            while len(history) > self.n_step + 1:
                history.popleft()
            if len(history) == self.n_step + 1:
                yield tuple(history)
            self.rewards.append(reward)
            state = next_state
            self.action = action
    def rewards_steps(self):
        rewards_steps = self.rewards
        self.rewards = []
        return rewards_steps

# Implementing Experience Replay
class ReplayMemory:
    
    def __init__(self, n_steps, capacity):
        self.capacity = capacity
        self.n_steps = n_steps
        self.n_steps_iter = iter(n_steps)
        self.buffer = deque()

    def sample_batch(self, batch_size): # creates an iterator that returns random batches
        ofs = 0
        vals = list(self.buffer)
        np.random.shuffle(vals)
        while (ofs+1)*batch_size <= len(self.buffer):
            yield vals[ofs*batch_size:(ofs+1)*batch_size]
            ofs += 1

    def run_steps(self, samples):
        while samples > 0:
            entry = next(self.n_steps_iter) # x consecutive steps
            self.buffer.append(entry) # we put 1 for the current episode
            samples -= 1
        while len(self.buffer) > self.capacity: # we accumulate no more than the capacity
            self.buffer.popleft()

    def save_experience(self, path, name):
        with open(path + '/' + name, 'wb') as fp:
            pickle.dump(self.buffer, fp)
            
    def load_experience(self, path, name):
        if os.path.isfile(os.path.join(path, str(name))):
            print("=> loading experience... ")
            with open (path + '/' + name, 'rb') as fp:
                self.buffer = pickle.load(fp)
            print("Loading is complete !")
        else:
            print("no experience found...")
            exit(1)