# clang -O0 -emit-llvm helloworld.c -S -o filename.ll
#task   splash2x.water_spatial,  splash2x.water_nsquared,  splash2x.volrend  ,splash2x.radiosity
# splash2x.ocean_ncp  ,  splash2x.ocean_cp,  splash2x.fmm ,

import threading
from RL_brain_change_layer import DeepQNetwork
from change_random_system_env_set_affinity import *
#from model_change_reward.data_classify import *
import matplotlib.pyplot as plt
from data_classify import text_save

import numpy as np
import time
import random
import os
import sys
#random.seed(0)

#cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
#/home/ysg/下载/parsec-benchmark-master/bin
def run_maze(env):
    total_step = 100
    step = 0
    ENV,x,y =get_user_location(env.creat_ENV())
    observation = [[0,0]]
    observation1 = [0, 0]

    while step < total_step:
        sttp = 0
        app =0
        count = 0
        while count<20: #运行0到5
             action = RL.choose_action(step, observation) #强化学习，动作选择
             print("action",action)
             x_speed  , y_speed =env.get_action(action)
             print(x_speed,observation[0])
             observation_ = []
             observation_.append(observation1[0]+x_speed)
             observation_.append(observation1[1]+y_speed)
             reward = compute_reward(observation_,x,y)

             print("step",count)
             print("reward",reward)
             # text_save("data/data2/model_mean_yes_input_yes_f_c.txt", [np.mean(tem)]) #数据保存
             # text_save("data/data2/model_max_yes_input_yes_f_c", [max(tem)])
             # text_save("data/data2/model_action_yes_input_yes_f_c.txt", [tem[int(core)]])
             #
             print(observation,action,reward,observation_)
             RL.store_transition(observation, action, [[reward]], observation_) #记忆存储
             if (step > 100) and (step % 5 == 0):   #学习更新神经网络
                 RL.learn()
                 print("进入学习")
             observation = [observation_]
             print("obob",observation)
             count += 1

        step += 1
        print("step-----------",step)

    import matplotlib.pyplot as plt



    # plt.savefig('./max-tem_5000_.jpg')
    # plt.show()


if __name__ == "__main__":
    # maze game
    env = System_ENV(2,100,15)
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.6,
                      replace_target_iter=5,
                      memory_size=2000,
                      # output_graph=True
                      )
    run_maze(env)
    RL.plot_cost()

#

# blackscholes_run_time = [0.361,0.170,  1.592,0.754,  5.681, 3.085 ]  #3.272
# fluidanimate_run_time = [5.737,2.825,  11.765,5.951, 35.070,18.731]  ##20.389
# splash2x_fmm_run_time = [4.054,2.140,  17.670,9.571, 69.538,36.369]  #40.772
# splash2x_water_spatial_run_time = [4.867,2.335, 9.085,4.604, 34.446,18.264] #20.284
# x264_run_time = [1.314,0.482,  3.689,1.513, 9.693,5.190] #5.851
#
# latency_constrain =[0.3, 1.2, 4, 4.2, 8, 23]