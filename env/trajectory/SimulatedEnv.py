import os

from env.Env import BaseEnv
import pandas as pd
import numpy as np


class SimulatedEnv(BaseEnv):
    def __init__(self,
                 filepath,
                 start_point=(0, 0),
                 end_point=(100, 0),
                 latency=0.5,
                 md_number=10,
                 slot_number=20,
                 max_velocity=15) -> None:
        self.data = pd.read_csv(filepath, header=None)
        # MD Position
        idx_s = 0
        idx_e = (2 * md_number - 1)
        vals = self.data.loc[0, idx_s:idx_e].values
        md_position = np.reshape(vals, (2, md_number), order="F")
        super().__init__(md_position, start_point, end_point, latency, md_number, slot_number, max_velocity)

        # MD Tasks Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.tasks = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.tasks)

        # MD Rate Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.rate = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.rate)

        # UAV Trajectory Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + 2 * slot_number
        self.trajectory = np.reshape(self.data.loc[0, idx_s:idx_e].values, (2, slot_number), order="F")
        print(self.trajectory)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.task_type = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.task_type)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.bandwidth = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.bandwidth)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.frequency = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.frequency)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.offloading = np.reshape(self.data.loc[0, idx_s:idx_e].values, (md_number, slot_number), order="F")
        print(self.offloading)




if __name__ == '__main__':
    work_dir = '/Users/yulu/workspace/UAV_RL/data'
    file_path = os.path.join(work_dir, 'data.csv')
    senv = SimulatedEnv(file_path)
    senv
