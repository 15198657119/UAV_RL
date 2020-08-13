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
        self.n_action = 0
        self.n_features = 27
        self.__step = 1
        self.__action_space = []
        self.__trajectory = []
        self.__decision = []
        self.__velocity = []

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

        # 生成md_number位数的0-1向量全组合
        type = list(product(range(2), repeat=self.md_number))
        t_space = []

        # 生成速度空间
        for x in range(0, self.max_velocity):
            for y in range(-1 * self.max_velocity, self.max_velocity):
                val = sqrt(x ** 2 + y ** 2)
                if val <= self.max_velocity:
                    # a_space.append(Velocity(x, y, val))
                    # 将 速度空间和类型空间关联
                    for t in type:
                        t_space.append((x, y) + t)

        # a_space 只有速度
        # t_space 添加了类型
        self.n_action = len(a_space)
        self.__action_space = ActionSet(a_space)
        # self.n_action = len(t_space)
        # self.__action_space = ActionSet(t_space)

        return self.__action_space

    def get_action_space(self):
        return self.__action_space

    def doAction(self, idx):
        set = self.__action_space.action_space()
        return set[idx]

    def sample(self, n_sample=1):
        return self.__action_space.sample(n_sample)

    def close(self):
        self.__step = 1
        self.__trajectory = []
        self.__decision = []
        self.__velocity = []

    def __state_constraints(self, tasks, action, bandwidth, offloading, frequency):
        # 1. 判断约束条件是否满足 TODO
        # 获取当前位置和轨迹

        position = np.array(action.position).reshape(2, 1)
        decision = np.array(action.decision).reshape(self.md_number, 1)

        self.__trajectory.append(action.position)
        self.__decision.append(action.decision)

        self.__velocity.append((action.velocity.x, action.velocity.y))

        # 计算当前时间片的时延、速率等信息作为状态
        rate, distanze, channel_gain = self.__solution.infoDataRate(action.position, bandwidth)

        # 是否满足时间片时延约束
        s_tasks = tasks[:, self.__step - 1].reshape(self.md_number, 1)
        s_bandwidth = bandwidth[:, self.__step - 1].reshape(self.md_number, 1)
        s_offloading = offloading[:, self.__step - 1].reshape(self.md_number, 1)
        s_frequency = frequency[:, self.__step - 1].reshape(self.md_number, 1)
        latencyConstraint, latency = self.__solution.isUnderLatencyConstraint(s_tasks, action.position, s_bandwidth, decision, s_offloading, s_frequency)
        frequencyConstraint, f_total = self.__solution.isUnderFrequencyConstraint(decision, s_frequency)

        missionLatencyConstraint, mission_latency = self.__solution.isUnderMissionLatency(self.__trajectory, tasks, bandwidth, self.__decision, offloading, frequency)
        storageConstraint, md_total = self.__solution.isUnderMdStorage(self.__trajectory, tasks, bandwidth, self.__decision, offloading, frequency)
        uavStorageConstraint, uav_total = self.__solution.isUnderUavStorage(self.__trajectory, tasks, bandwidth, self.__decision, offloading, frequency)
        egyConstraint, egy_total, egy_cac, egy_exe, egy_fly = self.__solution.isUnderUavEnergy(self.__velocity, tasks, self.__decision, offloading, frequency)

        state = [position, s_tasks,
                 rate, distanze, channel_gain,
                 latency, latencyConstraint,
                 frequencyConstraint, f_total,
                 missionLatencyConstraint, mission_latency,
                 storageConstraint, md_total,
                 uavStorageConstraint, uav_total,
                 egyConstraint, egy_total, egy_cac, egy_exe, egy_fly]

        s = np.array([])
        for st in state:
            s = np.append(s, st)

        return s.tolist()

    def \
            step(self, action: Action):
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
        if self.__step > self.slot_number:
            raise Exception('超出规定步数')

        # 加载对应时间片数据
        m_trajectory = self.trajectory[:, 0:self.__step]
        m_tasks = self.tasks[:, 0:self.__step]
        m_bandwidth = self.bandwidth[:, 0:self.__step]
        m_frequency = self.frequency[:, 0:self.__step]
        m_offloading = self.offloading[:, 0:self.__step]
        m_types = self.task_type[:, 0:self.__step]

        # 加载对应时间片数据
        sol_point = self.trajectory[:, self.__step - 1]
        sol_tasks = self.tasks[:, self.__step - 1]
        sol_bandwidth = self.bandwidth[:, self.__step - 1]
        sol_frequency = self.frequency[:, self.__step - 1]
        sol_offloading = self.offloading[:, self.__step - 1]
        sol_types = self.task_type[:, self.__step - 1]

        # # 根据当前的时间片和位置计算奖励值
        # # x,y为时间片终点位置
        x_start = action.position[0]
        y_start = action.position[1]
        #
        x_end = x_start + action.velocity.x * self.latency
        y_end = y_start + action.velocity.y * self.latency
        #
        # action_vel = action.velocity  # 时间片速度
        # action_end = (action.position[0] + action_vel.x * self.latency, action.position[1] + action_vel.y * self.latency)

        # 时间片终止
        if self.__step == (self.slot_number - 1) and x_start == self.end_point[0] and y_start == self.end_point[1]:  # UAV到达了终点
            done = True

        uav_position = np.array((x_start, y_start))

        # 2. 计算能耗和轨迹奖励

        #if 0 <= x <= 100 and 0 <= y <= 100:
        #     energy = self.__solution.slotDeviceEnergy(sol_tasks, action.position, sol_types, sol_offloading,
        #                                               sol_bandwidth)
        #     e_reward = (1 - energy)
        #     e_reward = e_reward * 100
        #
        #     dis = np.linalg.norm(action.position - sol_point, ord=1)
        #     print("action.position - (100,0)",dis,self.__reward_radius,sol_point)
        #     #if dis <= self.__reward_radius:
        #     # if dis <= 50:
        #     #     # 时间片终点在范围内
        #     #     t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #     #     t_reward = t_reward * (self.__step + 90)
        #     #     if self.__step == 18 and dis == 0:
        #     #         t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #     #         t_reward = t_reward * 100000000000000
        #     #     elif self.__step == 18 and abs(uav_position.tolist()[0]- 100) <= 10  and uav_position.tolist()[1]<=10:
        #     #         t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #     #         t_reward = t_reward * 1000000000
        #     #     elif self.__step == 18 and abs(uav_position.tolist()[0]- 100) <= 20  and uav_position.tolist()[1]<=20:
        #     #         t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #     #         t_reward = t_reward * 10000
        #     #     elif self.__step == 18 and abs(uav_position.tolist()[0]- 100) <= 30  and uav_position.tolist()[1]<=30:
        #     #         t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #     #         t_reward = t_reward * 1000
        #     #
        #
        #
        #     if uav_position.tolist()[0] == 10 and uav_position.tolist()[1] == 0:
        #         # t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #         t_reward = 10000
        #     elif abs(uav_position.tolist()[0] - 100) <= 10 and uav_position.tolist()[1] <= 10:
        #         # t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #         t_reward = 1000
        #     elif abs(uav_position.tolist()[0] - 100) <= 30 and uav_position.tolist()[1] <= 30:
        #         # t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #         t_reward = 100
        #     elif abs(uav_position.tolist()[0] - 100) <= 50 and uav_position.tolist()[1] <= 50:
        #         # t_reward = (self.__reward_radius - dis) / self.__reward_radius
        #         t_reward = 10
        #     else:
        #         t_reward = 0
        # else:
        #     e_reward = -1000
        #     t_reward = -1000
        #
        # # 3. 返回相关信息
        observation = np.array([])
        vals = (uav_position, sol_tasks, rate, task_latency, isUnderLatencyConstraint, isUnderFrequencyConstraint)
        for val in vals:
            observation = np.append(observation, val)
        #
        # #reward = 0.2 * t_reward + 0.8 * e_reward
        # reward = 2 * t_reward
        if 0 <= x <= 100 and 0 <= y <= 100:
            if uav_position.tolist()[0] == 100\
                    and uav_position.tolist()[1] == 0:
                # t_reward = (self.__reward_radius - dis) / self.__reward_radius
                t_reward = 10000
            elif abs(uav_position.tolist()[0] - 100) <= 10 and uav_position.tolist()[1] <= 10:
                # t_reward = (self.__reward_radius - dis) / self.__reward_radius
                t_reward = 1000
            elif abs(uav_position.tolist()[0] - 100) <= 30 and uav_position.tolist()[1] <= 30:
                # t_reward = (self.__reward_radius - dis) / self.__reward_radius
                t_reward = 100
            elif abs(uav_position.tolist()[0] - 100) <= 50 and uav_position.tolist()[1] <= 50:
                # t_reward = (self.__reward_radius - dis) / self.__reward_radius
                t_reward = 10
        else:
            t_reward = -1000
        return (done, t_reward, observation.tolist(), uav_position)

        if 0 <= x_start and x_start <= 100 and 0 <= y_start and y_start <= 100:
            energy, e_trn, e_cac, e_exe = self.__solution.slotDeviceEnergy(sol_tasks, action.position, sol_types, action.decision, sol_bandwidth)
            e_reward = (10 - energy)
            e_reward = e_reward * 100

            dis = np.linalg.norm(action.position - sol_point, ord=1)
            if dis <= self.__reward_radius:
                # 时间片终点在范围内
                t_reward = (self.__reward_radius - dis) / self.__reward_radius
                t_reward = t_reward * (self.__step + 90)
                if self.__step == 18 and dis == 0:
                    t_reward = (self.__reward_radius - dis) / self.__reward_radius
                    t_reward = t_reward * 10000

            else:
                t_reward = 0

        else:
            e_reward = -1000
            t_reward = -1000
        #
        # # 3. 返回相关信息

        observation = self.__state_constraints(m_tasks, action, m_bandwidth, m_offloading, m_frequency)
        reward = 0.2 * t_reward + 0.8 * e_reward

        self.__step += 1
        return (done, reward, observation, uav_position)



if __name__ == '__main__':
    work_dir = '/Users/yulu/workspace/UAV_RL/data'
    file_path = os.path.join(work_dir, 'data_1.csv')
    senv = SimulatedEnv(file_path)
    for eps in range(300):
        for i in range(1, 20 + 1):
            v = senv.sample()
            action = Action(velocity=Velocity(v[0], v[1]), position=(0, 0), decision=v[2:])
            senv.step(action)

        senv.close()
    #
    # from itertools import product
    #
    # lst = np.zeros(shape=(10, 2 ** 10))
    # lst = list(product([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], repeat=10))
