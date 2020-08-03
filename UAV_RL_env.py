import numpy as np
from change_random_system_env_set_affinity import *
def creat_ENV(array_depth):
    ENV =np.zeros((array_depth,array_depth))
    ENV[1][1] = 1
    return ENV

def get_action(action):

    return angle,speed


def fresh_ENV(env ,action):
    angle,speed = get_action(action)
    onservation = rander(env,action)
