import os
from math import sqrt

from env.Env import BaseEnv, ActionSet, Velocity, Action, Observation
import pandas as pd
import numpy as np
from itertools import product

from env.Solution import Solution


class SimulatedEnv(BaseEnv):

    def __init__(self,
                 filepath,
                 start_point=(0, 0),
                 end_point=(100, 0),
                 latency=0.5,
                 md_number=6,
                 slot_number=20,
                 max_velocity=15,
                 reward_radius=5,
                 energy_reward_coefficient=0.8,
                 trajectory_reward_coefficient=0.2) -> None:
        super().__init__(start_point, end_point, latency, md_number, slot_number, max_velocity)
        self.__load_csv_data(filepath, md_number, slot_number)

        self.__step = -1
        self.__action_space = []
        self.__trajectory = pd.DataFrame(np.zeros(shape=(2, slot_number)))

        self.__reward_radius = reward_radius
        self.__energy_reward_coefficient = energy_reward_coefficient,
        self.__trajectory_reward_coefficient = trajectory_reward_coefficient

        # 模拟求解,生成动作空间
        self.__solution = Solution(self.md_position, self.tasks, slot_number, latency)
        self.__generate_action_space()

    def __load_csv_data(self, filepath, md_number, slot_number):
        self.data = pd.read_csv(filepath, header=None)
        # row = np.random.randint(0, 9)
        row = 0
        # MD Position
        idx_s = 0
        idx_e = (2 * md_number - 1)
        vals = self.data.loc[row, idx_s:idx_e].values
        self.md_position = np.reshape(vals, (2, md_number), order="F")

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

    def __generate_task_types(self, md_number):
        pro = product(np.zeros(md_number), repeat=md_number)

    def sample(self, n_sample=1):
        return self.__action_space.sample(n_sample)

    def step(self, action: Action):
        """
        环境对Agent的回应
        :param action: Agent所采取的动作
        :return: (观察，奖励，是否成功等相关信息)
        """
        done = False
        t_reward = 0
        e_reward = 0
        t_ce = self.__trajectory_reward_coefficient
        e_ce = self.__energy_reward_coefficient

        print(self.__step)
        if self.__step < self.slot_number - 1:
            self.__step += 1  # 步数累加, 以slot_number数量作为一个周期
        else:
            self.__step = 0
            raise Exception('超出步数')

        # 加载对应时间片数据
        sol_point = self.trajectory[:, self.__step]
        sol_tasks = self.tasks[:, self.__step]
        sol_bandwidth = self.bandwidth[:, self.__step]
        sol_frequency = self.frequency[:, self.__step]
        sol_offloading = self.offloading[:, self.__step]
        sol_types = self.task_type[:, self.__step]

        # 根据当前的时间片和位置计算奖励值
        x = action.position[0]
        y = action.position[1]
        x = x + action.velocity.x * self.latency
        y = y + action.velocity.y * self.latency
        # action_vel = action.velocity  # 时间片速度
        # action_end = (action.position[0] + action_vel.x * self.latency, action.position[1] + action_vel.y * self.latency)

        # 时间片终止
        if self.__step == (self.slot_number - 1) and x == self.end_point[0] and y == self.end_point[1]:  # UAV到达了终点
            done = True

        uav_position = np.array((x, y))

        # 1. 判断约束条件是否满足 TODO
        # 是否满足时间片时延约束
        isUnderLatencyConstraint = self.__solution.isUnderLatencyConstraint(sol_tasks, uav_position, sol_bandwidth,
                                                                            sol_types, sol_offloading,
                                                                            sol_frequency)
        # 是否满足CPU频率约束
        isUnderFrequencyConstraint = self.__solution.isUnderFrequencyConstraint(sol_types, sol_frequency)
        rate = self.__solution.slotDataRate(uav_position, sol_bandwidth)
        task_latency = self.__solution.slotLatency(task_size=sol_tasks,
                                                   uav_position=uav_position,
                                                   bandwidth=sol_bandwidth, task_type=sol_types,
                                                   task_portion=sol_offloading,
                                                   allocated_frequency=sol_frequency)

        # 2. 计算能耗和轨迹奖励
        if 0 <= x <= 100 and 0 <= y <= 100:
            energy = self.__solution.slotDeviceEnergy(sol_tasks, uav_position, sol_types, sol_offloading, sol_bandwidth)
            e_reward = (1 - energy)

            dis = np.linalg.norm(uav_position - sol_point, ord=1)
            if dis <= self.__reward_radius:
                # 时间片终点在范围内
                t_reward = (self.__reward_radius - dis) / self.__reward_radius
            else:
                t_reward = 0

        else:
            e_reward = -1
            t_reward = -1

        # 3. 返回相关信息
        observation = np.array([])
        vals = (uav_position, sol_tasks, rate, task_latency, isUnderLatencyConstraint, isUnderFrequencyConstraint)
        for val in vals:
            observation = np.append(observation, val)

        # observation = Observation(uav_position=uav_position, task_size=sol_tasks, data_rate=rate,
        #                           task_latency=task_latency,
        #                           constraints=(isUnderLatencyConstraint, isUnderFrequencyConstraint))

        reward = 0.2 * t_reward + 0.8 * e_reward

        return (done, reward, observation)


if __name__ == '__main__':
    work_dir = '/Users/yulu/workspace/UAV_RL/data'
    file_path = os.path.join(work_dir, 'data_1.csv')
    senv = SimulatedEnv(file_path)

    for i in range(0, 20):
        v = senv.sample()
        current_position = (0, 0)

        print(senv.step(Action(velocity=v, position=current_position)))
    #
    # from itertools import product
    #
    # lst = np.zeros(shape=(10, 2 ** 10))
    # lst = list(product([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], repeat=10))
