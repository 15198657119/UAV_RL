import os

from env.Env import BaseEnv
from env.Solution import Solution
import pandas as pd
import numpy as np

from env.trajectory.SimulatedEnv import SimulatedEnv


class SimulatedSolution(Solution):
    def __init__(self, env: SimulatedEnv, name='solution') -> None:
        super().__init__(name)
        self.env = env

    def solve(self):
        return (self.env.rate,
                self.env.trajectory,
                self.env.task_type,
                self.env.offloading,
                self.env.bandwidth,
                self.env.frequency)


if __name__ == '__main__':
    work_dir = './UAV_RL/data'
    file_path = os.path.join(work_dir, 'data.csv')
    senv = SimulatedEnv(file_path)

    ssol = SimulatedSolution(senv)
    ssol.solve()
