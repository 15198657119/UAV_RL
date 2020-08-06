"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
print(144%14 +1 )
print(int(144/14) +1)
import numpy as np
import math
#$from UAV_RL_env import creat_ENV
import numpy
import time
import sys
import subprocess
#from s_tuii.Sources.RaplPowerSource import *
#from freq_setting_tool_master.cat_get_cpu_freq import *
#from freq_setting_tool_master.new_freq_set import *
#from freq_setting_tool_master.system_env_set_affinity import *
#from freq_setting_tool_master.set_affinity import *
#from freq_setting_tool_master.get_tempature  import  get_mean_Tem
#from freq_setting_tool_master.get_tempature  import  get_core_Tem
#from freq_setting_tool_master.k_means import output_state_type
#from freq_setting_tool_master.k_means import *
#from freq_setting_tool_master.get_tempature i12mport get_Tem
#from
#  矩阵单位米
#  最大速度 15M/s

class System_ENV(object):
    def __init__(self,n_feature,array_depth,max_speed):
        self.action_space = ["move","hover"]
        self.max_speed = max_speed
       # self.action_space = action_space
        self.n_actions = 351 #定义动作空间大小为 （角度 * 无人机可用速度 + 悬停）
        self.n_features = n_feature
        self.array_depth = array_depth
        self.ENV = np.zeros((self.array_depth, self.array_depth))

    def creat_ENV(self):
        ENV = np.zeros((self.array_depth, self.array_depth))
        ENV[0][99] = 1
        return ENV

    def get_action(self,action):
        x_max_speed = 14
        y_max_speed = 5
        max_action_space = 351
        len = x_max_speed * y_max_speed
        if action == max_action_space:                         #x , y速度均为0  悬停
            x_speed = max_action_space - 2
            y_speed = max_action_space - 2
        elif action < len:                         #x y 轴均为正速度  x: 0-15m/s    y: 0-4m/s
            x_speed = int (action / x_max_speed)
            y_speed = action % x_max_speed

        elif (len <= action and action <= len *2):        #x y 轴均为正速度  y: 0-15m/s    x: 0-4m/s
            y_speed = int(action /x_max_speed ) % y_max_speed
            x_speed = action % x_max_speed

        elif ( len*2 < action and action < len*3):         #y轴正速度  x为负速度  x: -（0-15）m/s    y: 0-4m/s
            y_speed = int(action /x_max_speed ) % y_max_speed
            x_speed = - (action % x_max_speed)-3

        elif (len*3 <= action and action <= len*4):   #y轴正速度  x为负速度  x: -（0-15）m/s    y: 0-4m/s
            y_speed = - (int(action / x_max_speed) % y_max_speed)-3
            x_speed = action % x_max_speed
        elif (len*4 < action and action <= len * 5):     #y轴负速度  x为负速度  x: -（0-15）m/s    y: -（0-4m）/s
            y_speed = - (int(action / x_max_speed) % y_max_speed)-3
            x_speed = -(action % x_max_speed)-4
        return x_speed+2,y_speed+2

    def rander(self):
        return self.ENV

    def fresh_ENV(self,angle,speed):
        onservation = rander(self, angle,speed)
        #根据角度和速度来刷新环境

    def get_init_state(self,):
        return 0


# ENV=System_ENV(100,20,15)
# for i in range(350):
#     if i ==140:
#         print("######################################################################################################## ")
#     print(ENV.get_action(i))

# print(ENV.creat_ENV())
def get_user_location(ENV_array):
    print("输入所有用户横坐标：")
    x = list(map(int, input().split()))
    print("输入所有用户纵坐标：")
    y = list(map(int, input().split()))
    for i in range(len(x)):
        if len(x) != len(y):
            print("输入用户有误！")
        else :
            ENV_array[x[i]][y[i]] = 1
    return ENV_array,x,y


import math
def  compute_reward(observation_,x,y):
    # if observation_[0]<0 or observation_[1]<0 or observation_[0]>100 or observation_[1]>100:
    #     reward = -1000
    # else:
    if (observation_[0] == x[0] and observation_[1] == y[0]):
        reward = 10000
    elif ((x[0]-observation_[0]) <10 and (y[0]-observation_[1])<10) :
        reward = 100
    elif observation_[0]>100 or observation_[1]>100  or observation_[0]<0 or observation_[1]<0 :
        reward = -10000
    else:
        reward = ((observation_[0]-x[0]) * (observation_[0]-x[0])  +  (observation_[1]-y[0])* (observation_[1]-y[0]) )
        reward = -math.sqrt(reward)
    return reward


def step_all(ob,x,y):
    ob1=[]
    ob1.append(ob[0]+x)
    ob1.append(ob[1]+y)
    return  ob1

# print(get_user_location(ENV.creat_ENV()))


#
# class System_ENV(object):
#     def __init__(self,n_feature,array_depth,max_speed):
#         self.action_space = ["move","hover"]
#         self.max_speed = max_speed
#        # self.action_space = action_space
#         self.n_actions = self.max_speed * 360 + 1   #定义动作空间大小为 （角度 * 无人机可用速度 + 悬停）
#         self.n_features = n_feature
#         self.array_depth = array_depth
#         self.ENV = np.zeros((self.array_depth, self.array_depth))
#
#     def creat_ENV(self):
#         ENV = np.zeros((self.array_depth, self.array_depth))
#         ENV[1][1] = 1
#         return ENV
#
#     def get_action(self,action):
#         if action == (self.max_spped * 360 + 1):
#             angle = 0
#             speed = 0
#         else:
#             angle =  action % self.n_actions
#             speed = int(action / 360)
#         return angle, speed
#
#     def rander(self):
#         return self.ENV
#
#     def fresh_ENV(self,angle,speed):
#         onservation = rander(self, angle,speed)
#         #根据角度和速度来刷新环境
#
#     def get_init_state(self,):
#         return 0
#
#
# ENV=System_ENV(100,20,15)
# def get_user_location(ENV_array):
#     print("输入所有用户横坐标：")
#     x = list(map(int, input().split()))
#     print("输入所有用户纵坐标：")
#     y = list(map(int, input().split()))
#     for i in range(len(x)):
#         if len(x) != len(y):
#             print("输入用户有误！")
#         else :
#             ENV_array[x[i]][y[i]] = 1
#     return ENV_array,x,y
#
# print(get_user_location(ENV.creat_ENV()))
