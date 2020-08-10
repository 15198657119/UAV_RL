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
from Solution import *

# from model_change_reward.data_classify import *

from game_self import show1


def run_maze(env):
    step = 0
    #ENV, x, y = get_user_location(env.creat_ENV())
    x=[100]
    y=[100]
    while step < 10000:
        env = env
        step1 = 0
        #ENV = ENV
        x = x
        y = y
        # print(ENV,x,y)
        observation = [[0, 100]]
        observation1 = [0, 100]


        count = 0
        location = []
        while True:  #
            action = RL.choose_action(step, observation)  # 强化学习，动作选择
            print("action", action)
            # 根据选择的动作映射出 x，y的飞行方向和速度
            x_speed, y_speed = env.getaction1(action)
            observation_ = step_all(observation1, x_speed, y_speed)
            location.append(observation1)
            observation1 = observation_

            show1(observation_, x_speed, y_speed)
            print("ob  x_speed y_speed ob_", observation, x_speed, y_speed, observation_)
            reward = compute_reward(observation_, x, y)
            all_reward.append(reward)

            print("memory", observation, action, reward, observation_)
            RL.store_transition(observation, action, [[reward]], observation_)

            if (step1 > 200) and (step1 % 5 == 0):
                RL.learn()
            step1 += 1
            # swap observation

            count += 1
            print("count", count)
            observation = [observation_]
            # 当步数多余20时不满足退出，飞出限定区域不满足退出
            if count > 20 or observation_[0]<0 or observation_[1]<0 or observation_[1]>100 or observation_[0]>100:
                break
            if count == 20 and reward>=100:
                print("保存轨迹")
                text_save("location.txt", [location])
            # if observation_[0] > 100 or observation_[1] > 100 or observation_[0] < 0 or observation_[1] < 0 :
            #     break
                # text_save("data/data2/model_mean_yes_input_yes_f_c.txt", [np.mean(tem)]) #数据保存

            # text_save("data/data2/model_action_yes_input_yes_f_c.txt", [tem[int(core)]])

        step += 1




if __name__ == "__main__":
    # maze game
    env = System_ENV(2, 100, 15)
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )
    all_reward = []
    run_maze(env)
    import matplotlib.pyplot as plt
    plt.plot(all_reward)
    plt.show()
    RL.plot_cost()
