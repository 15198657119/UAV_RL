import numpy as np

from env.Env import BaseEnv


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

    def reset(self):
        """
        重置环境：
            1. 随机生成任务矩阵
            2. 使用CVX计算UAV飞行轨迹
        :return:
        """
        self.__tasks = np.random.randint(100, 200, size=(self.__md_number, self.__slot_number)) / 1024

        # 使用CVX计算UAV的轨迹等数据

    def sample(self):
        pass

    def step(self, action):
        """
        环境对Agent的回应
        :param action: Agent所采取的动作
        :return: (观察，奖励，是否成功等相关信息)
        """
        self.__step += 1  # 步数累加

        if self.__step == self.__slot_number:
            # 时间片终止
            if action.position == 0:
                # UAV如果到达了终点
                done = True
            else:
                # UAV最后一个时间没有到达终点
                done = False

        # 根据当前的时间片和位置计算奖励值

    pass
