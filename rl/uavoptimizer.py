from RL_brain_change_layer import DeepQNetwork
from change_random_system_env_set_affinity import *
from env.Env import Action
from game_self import show1
import matplotlib.pyplot as plt
from env.trajectory.SimulatedEnv import SimulatedEnv
import os


def run_maze(env):
    step = 0

    while step < 2000:
        env = env
        step1 = 0
        ENV = ENV
        x = 100
        y = 0
        # print(ENV,x,y)
        observation = [[0, 0]]
        observation1 = [0, 0]

        all_reward = []
        count = 0
        while True:  #
            action = RL.choose_action(step, observation)  # 强化学习，动作选择
            print("action", action)
            # 根据选择的动作映射出 x，y的飞行方向和速度
            x_speed, y_speed = env.get_action(action)
            observation_ = step_all(observation1, x_speed, y_speed)

            done, reward, observation, uav_position = env.step(Action(position=(0, 0), velocity=(0, 0, 0)))


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
            if count > 20:
                break
            # text_save("data/data2/model_mean_yes_input_yes_f_c.txt", [np.mean(tem)]) #数据保存
            # text_save("data/data2/model_max_yes_input_yes_f_c", [max(tem)])
            # text_save("data/data2/model_action_yes_input_yes_f_c.txt", [tem[int(core)]])

        step += 1

    plt.plot(all_reward)
    plt.show()


if __name__ == "__main__":
    # create simulated environment
    filepath = '/home/bly/Workspace/UAV_RL/data'
    filepath = os.path.join(filepath, 'data_1.csv')
    env = SimulatedEnv(filepath)
    done, reward, observation, uav_position = env.step(Action(position=(0, 0), velocity=(0, 0, 0)))

    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )
    run_maze(env, observation)
    RL.plot_cost()
