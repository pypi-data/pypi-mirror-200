import pytest

from simpleoptions.option import BaseOption
from simpleoptions.options_agent import OptionAgent
from simpleoptions.environment import BaseEnvironment


class DummyLowerLevelOption(BaseOption):
    def __init__(self):
        super.__init__()

    def initiation(self, state):
        return state not in [3, 6]

    def policy(self, state):
        return 1

    def termination(self, state):
        return state in [3, 6]

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()

    def __hash__(self):
        return super()

    def __eq__(self, __o):
        return super().__eq__(__o)

    def __ne__(self, __o: object):
        return super().__ne__(__o)


class DummyHigherLevelOption(BaseOption):
    def __init__(self):
        super.__init__()

    def initiation(self, state):
        return super().initiation()

    def policy(self, state):
        return super().policy(state)

    def termination(self, state):
        return super().termination(state)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, __o):
        return super().__eq__(__o)

    def __ne__(self, __o: object):
        return super().__ne__(__o)


class DummyEnv(BaseEnvironment):
    def __init__(self):
        super().__init__()

    def reset(self, state=None):
        self.state = 1
        return 1

    def step(self, action, state=None):

        if action == 0:
            self.state = max(1, self.state - 1)
        elif action == 1:
            self.state = min(6, self.state + 1)

        if self.state == 6:
            reward = 1.0
            terminal = True
        else:
            reward = -0.1
            terminal = False

        return self.state, reward, terminal, {}

    def get_action_space(self):
        return [0, 1]

    def get_available_actions(self, state=None):
        return self.get_action_space()

    def is_state_terminal(self, state=None):
        if state is None:
            return self.state == 6
        else:
            return state == 6

    def get_initial_states(self):
        return [0]

    def get_successors(self, state=None):
        if state is None:
            return [max(0, self.state - 1), min(6, self.state + 1)]
        else:
            return [max(0, state - 1), min(6, state + 1)]
