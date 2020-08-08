import os
from math import sqrt

from env.Env import BaseEnv, ActionSet, Velocity, Action
import pandas as pd
import numpy as np

from env.Solution import Solution


class SimulatedEnv(BaseEnv):

    def __init__(self,
                 filepath,
                 start_point=(0, 0),
                 end_point=(100, 0),
                 latency=0.5,
                 md_number=10,
                 slot_number=20,
                 max_velocity=15,
                 reward_radius=5,
                 energy_reward_coefficient=0.8,
                 trajectory_reward_coefficient=0.2) -> None:

        self.__step = 0
        self.__action_space = []
        self.__reward_radius = reward_radius
        self.__energy_reward_coefficient = energy_reward_coefficient,
        self.__trajectory_reward_coefficient = trajectory_reward_coefficient
        self.data = pd.read_csv(filepath, header=None)
        row = np.random.randint(0, 9)
        # MD Position
        idx_s = 0
        idx_e = (2 * md_number - 1)
        vals = self.data.loc[row, idx_s:idx_e].values
        md_position = np.reshape(vals, (2, md_number), order="F")
        super().__init__(md_position, start_point, end_point, latency, md_number, slot_number, max_velocity)

        # MD Tasks Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.tasks = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")
        # print(self.tasks)

        # MD Rate Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.rate = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")
        # print(self.rate)

        # UAV Trajectory Matrix
        idx_s = idx_e + 1
        idx_e = idx_e + 2 * slot_number
        self.trajectory = np.reshape(self.data.loc[row, idx_s:idx_e].values, (2, slot_number), order="F")
        # print(self.trajectory)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.task_type = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")
        # print(self.task_type)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.bandwidth = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")
        # print(self.bandwidth)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.frequency = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")
        # print(self.frequency)

        idx_s = idx_e + 1
        idx_e = idx_e + md_number * slot_number
        self.offloading = np.reshape(self.data.loc[row, idx_s:idx_e].values, (md_number, slot_number), order="F")

        self.__solution = Solution(self.md_position, self.tasks, slot_number, latency)

        # print(self.offloading)
        self.__generate_action_space()

    def __generate_action_space(self) -> ActionSet:
        """
        创建动作空间
        """
        # 单个时间片内可飞行的最大距离
        # 假设飞行速度为矢量(x,y)，且在x/y轴的方向可正可负
        # max_distance = self.__max_velocity * self.__latency

        a_space = []

        for x in range(-1 * self.max_velocity, self.max_velocity):
            for y in range(-1 * self.max_velocity, self.max_velocity):
                val = sqrt(x ** 2 + y ** 2)
                if val <= self.max_velocity:
                    a_space.append(Velocity(x, y, val))

        self.__action_space = ActionSet(a_space)

        return self.__action_space

    def get_action_space(self):
        return self.__action_space

    def sample(self, n_sample=1):
        return self.__action_space.sample(n_sample)

    def step(self, action: Action):
        """
        环境对Agent的回应
        :param action: Agent所采取的动作
        :return: (观察，奖励，是否成功等相关信息)
        """
        self.__step = 1
        done = False
        t_reward = 0
        e_reward = 0
        t_ce = self.__trajectory_reward_coefficient
        e_ce = self.__energy_reward_coefficient

        sol_point = self.trajectory[:, self.__step]
        sol_tasks = self.tasks[:, self.__step - 1]
        sol_bandwidth = self.bandwidth[:, self.__step - 1]
        sol_frequency = self.frequency[:, self.__step - 1]
        sol_offloading = self.offloading[:, self.__step - 1]
        sol_types = self.task_type[:, self.__step - 1]

        action_end = action.p_end  # 时间到达点
        action_vel = action.velocity  # 时间片速度

        self.__step += 1  # 步数累加
        if self.__step == self.slot_number:
            # 时间片终止
            if action.p_start == 0:
                # UAV如果到达了终点
                done = True
            else:
                # UAV最后一个时间没有到达终点
                done = False

        # 根据当前的时间片和位置计算奖励值
        x = action.p_start[0]
        y = action.p_start[1]
        x = x + action.velocity.x * self.latency
        y = y + action.velocity.y * self.latency
        observation = (x, y)

        # 1. 判断约束条件是否满足 TODO

        # 2. 计算能耗和轨迹奖励
        dis = np.linalg.norm(np.array(action_end) - sol_point, ord=1)
        if dis <= self.__reward_radius:
            # 时间片终点在范围内
            t_reward = (self.__reward_radius - dis) / self.__reward_radius
        else:
            t_reward = 0

        if 0 <= x <= 100 and 0 < y <= 100:
            energy = self.__solution.slotDeviceEnergy(sol_tasks, sol_point, sol_types, sol_offloading, sol_bandwidth)
            e_reward = (20 - energy) / 20
        else:
            e_reward = 0

        # 3. 返回相关信息

        reward = 0.2 * t_reward + 0.8 * e_reward
        return (done, observation, reward)


if __name__ == '__main__':
    work_dir = '/Users/yulu/workspace/UAV_RL/data'
    file_path = os.path.join(work_dir, 'data.csv')
    senv = SimulatedEnv(file_path)

    v = senv.sample()
    ps = (0, 0)
    pe = (v.x * senv.latency, v.y * senv.latency)
    print(senv.step(Action(velocity=v, p_start=(0, 0), p_end=pe)))
