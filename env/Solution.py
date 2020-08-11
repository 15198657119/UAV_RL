import math

import numpy as np


class Solution:
    __bandwidth = 10
    __storage = 50
    __energy_budget = 10 ** 6
    __frequency = 5 * 10 ** 3
    __channel_power = -50
    __noise_pose = -130
    __transmit_power = 1

    # uav fly parameters
    __blade_power = 158.76
    __induced_power = 88.63
    __qtips = 120
    __rho = 1.225
    __rotor_disc_aera = 1
    __hover_induced_velocity = 4.03
    __fuselage_drag_ratio = 0.3
    __fuselage_rotor_solidity = 0.05
    __max_velocity = 15
    __height = 100

    # md parameter
    __md_transmit_power = 1
    __md_frequency = 100
    __md_storage = 1
    __md_number = 4
    __md_tasks = None
    __md_position = None
    __md_cache = 0.001

    __width = 100
    __latency = 0.5
    __slot = 20
    __Q0 = [0, 0]
    __QF = [0, 0]

    __ETA = 10 ** -6
    __BITS = 10 ** 3
    __CA = 0.015
    __TK = 10
    __UAV_CA = 0.00375

    def __init__(self, md_positions, tasks, slot_number, slot_length) -> None:
        super().__init__()
        self.__md_position = md_positions
        self.__md_number = tasks.shape[0]

        self.__slot = slot_number
        self.__latency = slot_length
        self.__md_tasks = tasks

    def solve(self):
        pass

    def Db2Dec(self, dB):
        '''
            dB 为矩阵
        '''
        dec = np.power(10, (dB / 10))
        return dec

    def Distance(self, trajectory):
        '''
            Distance 计算UAV到各个MD之间的距离

            @positions 维度为2*K
        '''

        _, slot_numb = trajectory.shape

        md_num = self.__md_number

        dis = np.zeros([md_num, slot_numb])
        mds = self.__md_position

        for i in range(0, slot_numb):
            temp = np.repeat(trajectory[:, i], md_num)
            temp = np.power(temp.reshape(2, md_num) - mds, 2)
            temp = temp[1, :] + temp[0, :] + self.__height ** 2
            dis[:, i] = np.sqrt(temp)

        return dis

    def DataRate(self, trajectory, band_portion):
        """
            DataRate 根据给定的带宽和轨迹计算MD设备的实际通讯速率
            @trajectory UAV轨迹矩阵
            @band_portion UAV分配给各个用户的带宽占比
        """
        distanze = self.Distance(trajectory)
        channel_gain = self.__transmit_power * 1000
        channel_gain = channel_gain * self.Db2Dec(self.__channel_power)
        channel_gain = channel_gain / distanze

        band = self.__bandwidth * band_portion
        denominator = (band * np.power(10, 6) * self.Db2Dec(self.__noise_pose))

        # band = band.reshape(self.__md_number, 1)
        # denominator = denominator.reshape(self.__md_number, 1)

        rate = band * np.log2(1 + channel_gain / denominator)
        return rate

    def mdCacheEnergy(self, bits):
        """
            根据比特述计算存储能耗
        """
        return bits * self.__md_cache

    def mdCacheEnergy(self, task_type, task_offloading_portion):
        """
            根据卸载的比特述计算存储能耗
        """
        egy = self.__md_cache * self.__md_tasks
        return (egy, egy.sum())

    def mdLocalComputingEnergy(self, task_type, task_offloading_portion):
        egy = task_type * self.__md_tasks * self.__ETA * (1 - task_offloading_portion) * self.__BITS * (
                self.__md_frequency ** 2)
        return (egy, egy.sum())

    def mdTransmitionEnergy(self, trajectory, bandwidth, task_portion):
        """
            mdTransmitionEnergy 计算所有用户的传输能耗

            @trajectory UAV轨迹
            @bandwidth UAV分配带宽矩阵
            @task_portion 用户卸载比例矩阵
        """
        rate = self.DataRate(trajectory, bandwidth)
        tran_latency = self.__md_tasks * task_portion / rate
        return (self.__md_transmit_power * tran_latency, (tran_latency * self.__md_transmit_power).sum())

    def uavCacheEnergy(self, task_size, task_type, task_offloading_portion):
        """
            uavCacheEnergy 计算UAV的存储能耗

            @task_type 任务处理类型矩阵
            @task_offloading_portion 任务卸载比例矩阵

            @return (egy,egySum) 存储能耗矩阵，uav总存储能耗
        """

        egy = self.__UAV_CA * (1 - task_type) * task_offloading_portion * task_size
        return egy.sum(), egy

    def uavComputingEnergy(self, task_size, task_type, task_offloading_portion, allocated_frequency):
        """
            uavComputingEnergy 根据任务类型矩阵、任务卸载比例矩阵和分配的CPU矩阵计算UAV的计算能耗
            @task_type 任务处理类型矩阵 A
            @task_offloading_portion 任务卸载比例矩阵 L
            @allocated_frequency CPU分配矩阵 F

            @return (egy, egy.sum()) 各个任务的能耗和总能耗
        """
        egy = task_type * self.__ETA * task_offloading_portion * task_size * self.__BITS * (
                allocated_frequency ** 2)
        return egy.sum(), egy

    def uavFlyEnergy(self, velocity):
        """
            uavFlyEnergy 根据给定的速度向量计算UAV的飞行能耗

            @velocity UAV轨迹飞行速度向量
            @return egy UAV飞行所消耗的能耗
        """
        egy = self.__blade_power * (1 + 3 * np.power(velocity, 2) / (self.__qtips ** 2))
        temp = np.sqrt((1 + np.power(velocity, 4) / (4 * self.__hover_induced_velocity ** 4))) - (np.power(velocity, 2) / (2 * self.__hover_induced_velocity ** 2))
        egy = self.__induced_power * (np.sqrt(temp)) + egy
        egy = egy + 0.5 * self.__fuselage_drag_ratio * self.__fuselage_rotor_solidity * self.__rotor_disc_aera * self.__rho * np.power(velocity, 3)
        egy = egy.sum() * (self.__latency * self.__slot)

        return egy

    def localLatency(self, task_type, task_offloading_portion):
        """
            localLatency 计算任务的本地处理时间

            @task_type 任务类型 A
            @task_offloading_portion 任务卸载比例矩阵

            @return(latency) 本地处理时延矩阵
        """
        task_type * (1 - task_offloading_portion) * self.__md_tasks * self.__BITS / self.__md_frequency

    def offloadingLatency(self, trajectory, bandwidth, task_type, task_portion, allocated_frequency):
        """
            offloadingLatency 计算卸载任务时延

            @trajectory uav飞行轨迹
            @bandwidth uav带宽分配占比
            @task_type 任务类型矩阵
            @task_portion 任务卸载比例矩阵
            @allocated_frequency uav分配的计算资源矩阵

            @return(latency) 卸载到uav上的处理时延
        """
        rate = self.DataRate(trajectory, bandwidth)
        latency_transmition = self.__md_tasks * task_portion / rate
        latency_uavExecution = task_type * task_portion * self.__md_tasks * self.__BITS / allocated_frequency
        return latency_transmition + latency_uavExecution

    def taskLatency(self, trajectory, bandwidth, task_type, task_portion, allocated_frequency):
        """
            taskLatency 计算实际的处理时延

            @trajectory uav飞行轨迹
            @bandwidth uav带宽分配占比
            @task_type 任务类型矩阵
            @task_portion 任务卸载比例矩阵
            @allocated_frequency uav分配的计算资源矩阵

            @return(latency) 任务总的处理时延
        """

        loc = self.localLatency(task_type, task_portion)
        off = self.offloadingLatency(trajectory, bandwidth, task_type, task_portion, allocated_frequency)

        return np.maximum(loc, off)

    def slotDistance(self, uav_position):
        """

        """
        distanze = np.zeros(shape=(self.__md_number))
        md_position = self.__md_position

        temp = np.repeat(uav_position, self.__md_number).reshape(2, self.__md_number)
        temp = self.__md_position - temp

        for d in range(0, self.__md_number):
            x = temp[0, d]
            y = temp[1, d]

            distanze[d] = math.sqrt(x ** 2 + y ** 2 + self.__height ** 2)
        return distanze

    def slotDataRate(self, p_uav, bandwidth):
        distanze = self.slotDistance(p_uav)
        channel_gain = self.__transmit_power * 1000
        channel_gain = channel_gain * self.Db2Dec(self.__channel_power)
        channel_gain = channel_gain / distanze

        band = self.__bandwidth * bandwidth
        denominator = (band * np.power(10, 6) * self.Db2Dec(self.__noise_pose))

        rate = band * np.log2(1 + channel_gain / denominator)
        return rate

    def infoDataRate(self, uav_position, bandwidth):
        distanze = self.slotDistance(uav_position)
        distanze = distanze.reshape(self.__md_number, 1)

        channel_gain = self.__transmit_power * 1000
        channel_gain = channel_gain * self.Db2Dec(self.__channel_power)
        channel_gain = channel_gain / distanze

        band = self.__bandwidth * bandwidth
        denominator = (band * np.power(10, 6) * self.Db2Dec(self.__noise_pose))

        rate = band * np.log2(1 + channel_gain / denominator)

        return rate, distanze, channel_gain

    def slotTranEnergy(self, task_size, task_portion, uav_position, bandwidth):
        rate = self.slotDataRate(uav_position, bandwidth)
        egy = self.__md_transmit_power * task_size * task_portion / rate
        return egy.sum()

    def slotDeviceEnergy(self, task_size, uav_position, task_type, offloading_portion, bandwidth):
        """
        mdEnergy 计算当前时间片MD的能耗和
        @uav_position UAV当前位置
        @task_type 卸载类型
        @offloading_portion 卸载比例
        @bandwidth 分配的带宽
        @frequency 分配的CPU
        """
        if offloading_portion is not np.ndarray:
            offloading_portion = np.array(offloading_portion)

        e_cac = (1 - task_type) * (1 - offloading_portion) * task_size * self.__CA
        e_cac = e_cac.sum()

        e_exe = self.__ETA * self.__BITS * (self.__md_frequency ** 2)
        e_exe = task_type * (1 - offloading_portion) * task_size * e_exe
        e_exe = e_exe.sum()

        e_trn = self.slotTranEnergy(task_size, offloading_portion, uav_position, bandwidth)

        # e_trn_matrix, e_trn = self.mdTransmitionEnergy(uav_position, bandwidth, offloading_portion)

        return e_trn + e_cac + e_exe, e_trn, e_cac, e_exe

    def slotLocalLatency(self, task_size, task_type, offloading_portion):
        latency = task_type * (1 - offloading_portion) * task_size * self.__BITS / self.__md_frequency
        return latency

    def slotOffloadingLatency(self, task_size, uav_position, bandwidth, task_type, task_portion, allocated_frequency):
        rate = self.slotDataRate(uav_position, bandwidth)
        latency_trn = task_size * task_portion / rate
        latency_exe = task_type * task_size * task_portion * self.__BITS / allocated_frequency
        return latency_exe + latency_trn

    def slotLatency(self, task_size, uav_position, bandwidth, task_type, task_portion, allocated_frequency):
        loc = self.slotLocalLatency(task_size, task_type, task_portion)
        off = self.slotOffloadingLatency(task_size, uav_position, bandwidth, task_type, task_portion,
                                         allocated_frequency)

        return np.maximum(loc, off)

    def isUnderLatencyConstraint(self, task_size, uav_position, bandwidth, task_type, task_portion,
                                 allocated_frequency):

        if uav_position is not np.ndarray:
            uav_trajectory = np.array(uav_position).reshape(2, 1)

        rate = self.DataRate(uav_trajectory, bandwidth)
        latency_trn = task_size * task_portion / rate
        latency_exe = task_type * task_portion * task_size * self.__BITS / allocated_frequency
        off = latency_trn + latency_exe

        loc = task_type * (1 - task_portion) * task_size * self.__BITS / self.__md_frequency

        latency = np.maximum(off, loc)
        latencyConstraint = (latency <= self.__latency)

        return latencyConstraint, latency

    def isUnderFrequencyConstraint(self, task_type, allocated_frequency):
        total = task_type * allocated_frequency
        total = total.sum()
        frequencyConstraint = total <= self.__frequency
        return frequencyConstraint, total

    def isUnderMissionLatency(self, uav_trajectory, task_size, bandwidth, task_type, task_portion, allocated_frequency):
        if uav_trajectory is not np.ndarray:
            task_type = np.array(task_type).T
            uav_trajectory = np.array(uav_trajectory).T

        rate = self.DataRate(uav_trajectory, bandwidth)
        latency_trn = task_size * task_portion / rate
        latency_exe = task_type * task_portion * task_size * self.__BITS / allocated_frequency
        off = latency_trn + latency_exe

        loc = task_type * (1 - task_portion) * task_size * self.__BITS / self.__md_frequency
        latency = np.maximum(off, loc)
        # latency = latency
        mission_latency = latency.sum(axis=1)

        latencyConstraint = mission_latency <= self.__latency * self.__slot

        return latencyConstraint, mission_latency

    def isUnderUavStorage(self, uav_trajectory, task_size, bandwidth, task_type, task_portion, allocated_frequency):
        if task_type is not np.ndarray:
            task_type = np.array(task_type).T

        n_tasks = (1 - task_type) * task_portion * task_size
        n_total = n_tasks.sum()

        return n_total <= self.__storage, n_total

    def isUnderMdStorage(self, uav_trajectory, task_size, bandwidth, task_type, task_portion, allocated_frequency):
        if task_type is not np.ndarray:
            task_type = np.array(task_type).T

        n_tasks = (1 - task_type) * (1 - task_portion) * task_size
        n_total = n_tasks.sum(axis=1)

        storageConstraint = n_total <= self.__md_storage
        return storageConstraint, n_total

    def isUnderUavEnergy(self, velocity, task_size, task_type, task_portion, allocated_frequency):
        if task_type is not np.ndarray:
            task_type = np.array(task_type).T
            velocity = np.array(velocity).T

        egy_exe, _ = self.uavComputingEnergy(task_size, task_type, task_portion, allocated_frequency)
        egy_cac, _ = self.uavCacheEnergy(task_size, task_type, task_portion)
        egy_fly = self.uavFlyEnergy(velocity)

        egy_total = egy_cac + egy_exe + egy_fly
        egyConstraint = egy_total <= self.__energy_budget

        return egyConstraint, egy_total, egy_cac, egy_exe, egy_fly
