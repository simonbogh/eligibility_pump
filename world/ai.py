from abc import ABCMeta, abstractmethod

from world.ai_input_provider import AiInputProvider


class AI:
    def __init__(self, params, dqn_initializator):
        self.brain = dqn_initializator(params, AiActionProvider.NUMBER_OF_ACTIONS)

    def get_next_action(self, input):
        action = self.brain.update(input)
        return AiActionProvider.ACTIONS[action]

    def score(self):
        return self.brain.score()


class AiAction:
    __metaclass__ = ABCMeta

class AiActionProvider:
    ACTIONS = [1, 2, 3]
    NUMBER_OF_ACTIONS = len(ACTIONS)
