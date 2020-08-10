from RL_brain_change_layer import DeepQNetwork
from change_random_system_env_set_affinity import *
# from model_change_reward.data_classify import *
from env.Env import Action, Velocity
from game_self import show1
import matplotlib.pyplot as plt
from env.trajectory.SimulatedEnv import SimulatedEnv
import os


def run_maze(env, observation, uav_position):
    step = 0

    while step < 2000:
        step1 = 0
        all_reward = []
        count = 0

        print("step ", step)

        while True:  #

            print("begin", observation)
            action = RL.choose_action(step, [observation])  # 强化学习，动作选择
            print("action", action)
            # 根据选择的动作映射出 x，y的飞行方向和速度
            velocity = env.doAction(action)
            x = velocity.x
            y = velocity.y
            v = velocity.val
            # observation_ = step_all(observation1, x_speed, y_speed)

            done, reward, observation_, uav_position = env.step(
                Action(position=uav_position, velocity=Velocity(x=x, y=y, val=math.sqrt(x ** 2 + y ** 2))))
            uav_x = uav_position
            observation1 = observation_
            # show1(uav_position, x, y)
            print("ob  x_speed y_speed ob_", observation, x, y, observation_)
            # reward = compute_reward(observation_, x, y)
            all_reward.append(reward)

            print("memory", observation, action, reward, observation_)
            RL.store_transition([observation], [[action]], [[reward]], [observation_])

            if (step1 > 200) and (step1 % 5 == 0):
                RL.learn()
            step1 += 1
            # swap observation

            count += 1
            print("count", count)
            observation = observation_
            # 当步数多余20时不满足退出，飞出限定区域不满足退出
            if count > 18:
                env.close()
                break
            # text_save("data/data2/model_mean_yes_input_yes_f_c.txt", [np.mean(tem)]) #数据保存
            # text_save("data/data2/model_max_yes_input_yes_f_c", [max(tem)])
            # text_save("data/data2/model_action_yes_input_yes_f_c.txt", [tem[int(core)]])

        step += 1

    plt.plot(all_reward)
    plt.show()


if __name__ == "__main__":
    # create simulated environment
    work_dir = 'C:\\Users\\86151\\Desktop\\liwentao\\data'
    file_path = os.path.join(work_dir, 'data_1.csv')
    env = SimulatedEnv(file_path)

    done, reward, observation, uav_position = env.step(Action(position=(0, 0), velocity=Velocity(x=0, y=0, val=0)))
    n_features = len(observation)
    RL = DeepQNetwork(env.n_action, n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )
    run_maze(env, observation, uav_position)
    RL.plot_cost()
