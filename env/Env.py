from collections import namedtuple

import numpy as np


class BaseEnv(object):
    def __init__(self,
                 md_position,
                 start_point=(0, 0),
                 end_point=(100, 0),
                 latency=0.5,
                 md_number=4,
                 slot_number=20,
                 max_velocity=15, ) -> None:
        super().__init__()
        self.md_position = md_position
        self.tasks = np.random.randint(100, 200, size=(md_number, slot_number)) / 1024
        self.latency = latency
        self.md_number = md_number
        self.slot_number = slot_number
        self.start_point = start_point
        self.end_point = end_point

        self.max_velocity = max_velocity

    def reset(self):
        pass

    def step(self):
        pass

    def sample(self, n_sample=1):
        pass


Velocity = namedtuple("velocity", ['x', 'y', 'val'])
Action = namedtuple('action', ['position', 'velocity'])


class ActionSet:

    def __init__(self, set) -> None:
        super().__init__()
        self.__action_set = set

    def sample(self, n_sample=1):
        """
            sample 对动作空间进行随机抽样

            @n_sample 抽样的数量,默认为1个
        """
        import random
        if n_sample == 1:
            idx = random.randint(0, len(self.__action_set) - 1)
            return self.__action_set[idx]
        else:
            sample = []
            for i in range(n_sample):
                idx = random.randint(0, len(self.__action_set))
                sample.append(self.__action_set[idx])

            return sample

    def action_space(self):
        return self.__action_set
