import numpy as np
from matplotlib import pyplot as plt

from DeepRacer.reward import reward_distance_from_center


TRACK_WIDTH_NEW = 5


def plot_distance_from_center_reward():
    x_points = []
    y_points = []

    for i in np.arange(0, TRACK_WIDTH_NEW + 3, 0.1):
        x_points.append(i)

    for x_point in x_points:
        reward = reward_distance_from_center(TRACK_WIDTH_NEW, True, False, x_point)
        y_points.append(reward)

    plt.plot(np.array(x_points), np.array(y_points))

    plt.title("Reward Distance to Center")
    plt.xlabel("Distance to Center")
    plt.ylabel("Reward")
    plt.show()
