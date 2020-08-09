import unittest
import numpy as np

from env.trajectory.UavTrajectoryEnv import UavTrajectoryEnv


class TestUavTrajectoryEnv(unittest.TestCase):
    def test_env_action_space(self):
        K = 4
        N = 20

        md_positions = np.random.randint(low=0, high=100, size=(2, K))
        env = UavTrajectoryEnv(md_positions)
        env.generate_action_space()

if __name__ == '__main__':
    unittest.main()
