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

def run_maze(env):
    step = 0
    ENV, x, y = get_user_location(env.creat_ENV())

    while step < 1000000:
        env = env
        step1 = 0
        ENV = ENV
        x = x
        y = y
        #print(ENV,x,y)
        observation = [[0, 0]]
        observation1 = [0, 0]
        ob=[0,0]
        all_reward = []
        count =0
        while (count <20 and ob[0]<100 and  ob[1]<100 ) :  #
            action = RL.choose_action(step, observation)  # 强化学习，动作选择
            print("action", action)
            x_speed, y_speed = env.get_action(action)
            print(x_speed, observation[0])
            observation_ = [0,0]
            print( observation_[0],   observation1[0])
            observation_[0]=(observation1[0] + x_speed)
            observation_[1]=(observation1[1] + y_speed)
            # observation_.append(observation1[0] + x_speed)
            # observation_.append(observation1[1] + y_speed)
            print("ob  x_speed y_speed",observation,x_speed,y_speed)
            reward = compute_reward(observation_, x, y)
            reward= - reward
            all_reward.append(reward)
            print("step", count)
            print("reward", reward)
            # text_save("data/data2/model_mean_yes_input_yes_f_c.txt", [np.mean(tem)]) #数据保存
            # text_save("data/data2/model_max_yes_input_yes_f_c", [max(tem)])
            # text_save("data/data2/model_action_yes_input_yes_f_c.txt", [tem[int(core)]])

            print(observation, action, reward, observation_)
            RL.store_transition(observation, action,[[reward]], observation_)

            if (step1 > 200) and (step1 % 5 == 0):
                RL.learn()
            step1 +=1
            # swap observation
            observation = observation_
            observation1 = observation_
            ob=observation

            count +=  1
            print("count",count)
            observation = [observation]
            all_reward.append(reward)
        step += 1


    import matplotlib.pyplot as plt
    plt.plot(all_reward)
    plt.show()

if __name__ == "__main__":
    # maze game
    env = System_ENV(2,100,15)
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    run_maze(env)
    RL.plot_cost()