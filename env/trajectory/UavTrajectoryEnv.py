from collections import namedtuple
from math import sqrt

import numpy as np

from env.Env import BaseEnv

Velocity = namedtuple("velocity", ['x', 'y', 'val'])
Action = namedtuple('action', ['p_start', 'p_end', 'velocity'])


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
            idx = random.randint(0, len(self.__action_set))
            return self.__action_set[idx]
        else:
            sample = []
            for i in range(n_sample):
                idx = random.randint(0, len(self.__action_set))
                sample.append(self.__action_set[idx])

            return sample

    def action_space(self):
        return self.__action_set


class UavTrajectoryEnv(BaseEnv):
    __step = 0  # 操作步数记录

    def __init__(self, md_position,
                 start_point=(0, 0),
                 end_point=(100, 0),
                 latency=0.5,
                 md_number=4,
                 slot_number=20,
                 max_velocity=15,
                 reward_radius=20,
                 energy_reward_coefficient=0.8,
                 trajectory_reward_coefficient=0.2) -> None:
        """
        创建环境，随机生成MD设备的任务矩阵(md_number,slot_number)

        :param md_position: MD设备的位置矩阵 (2,K)
        :param start_point: UAV起点
        :param end_point: UAV终点
        :param latency: 时延上限
        :param user_number: MD设备的数量
        :param slot_number: 时间片的数量

        :param max_velocity: UAV最大速度
        :param reward_radius: 轨迹奖励衰减半径
        :param energy_reward_coefficient: 能耗奖励权重
        :param trajectory_reward_coefficient: 轨迹奖励权重
        """

        super().__init__()
        self.__tasks = np.random.randint(100, 200, size=(md_number, slot_number)) / 1024
        self.__md_positions = md_position
        self.__latency = latency
        self.__md_number = md_number
        self.__slot_number = slot_number
        self.__start_point = start_point
        self.__end_point = end_point
        self.__max_velocity = 15

        self.__max_velocity = max_velocity
        self.__reward_radius = reward_radius
        self.__energy_reward_coefficient = energy_reward_coefficient,
        self.__trajectory_reward_coefficient = trajectory_reward_coefficient

    def generate_action_space(self) -> ActionSet:
        """
        创建动作空间
        """
        # 单个时间片内可飞行的最大距离
        # 假设飞行速度为矢量(x,y)，且在x/y轴的方向可正可负
        # max_distance = self.__max_velocity * self.__latency

        action_space = []

        for x in range(-1 * self.__max_velocity, self.__max_velocity):
            for y in range(-1 * self.__max_velocity, self.__max_velocity):
                val = sqrt(x ** 2 + y ** 2)
                if val <= self.__max_velocity:
                    action_space.append(Velocity(x, y, val))

        self.__action_space = ActionSet(action_space)

        return self.__action_space

    def reset(self):
        """
        重置环境：
            1. 随机生成任务矩阵
            2. 使用CVX计算UAV飞行轨迹
        :return:
        """
        self.__tasks = np.random.randint(100, 200, size=(self.__md_number, self.__slot_number)) / 1024

        # 使用CVX计算UAV的轨迹等数据

    def sample(self, n_sample=1):
        self.__action_space.sample(n_sample)

    def step(self, action: Action):
        """
        环境对Agent的回应
        :param action: Agent所采取的动作
        :return: (观察，奖励，是否成功等相关信息)
        """
        done = False
        t_reward = 0
        e_reward = 0

        self.__step += 1  # 步数累加
        if self.__step == self.__slot_number:
            # 时间片终止
            if action.p_start == 0:
                # UAV如果到达了终点
                done = True
            else:
                # UAV最后一个时间没有到达终点
                done = False

        # 根据当前的时间片和位置计算奖励值

        # 1. 判断约束条件是否满足
        # 2. 计算能耗和轨迹奖励
        # 3. 返回相关信息

        observation = ()
        info = ()

        reward = self.__trajectory_reward_coefficient * t_reward + self.__energy_reward_coefficient * e_reward
        return (done, observation, reward, info)


if __name__ == '__main__':
    K = 4
    N = 20

    md_positions = np.random.randint(low=0, high=100, size=(2, K))
    env = UavTrajectoryEnv(md_positions)
    actions = env.generate_action_space()
    set = ActionSet(actions)

    env.step(set.sample())
