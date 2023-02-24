import matplotlib.pyplot as plt
import numpy as np

from DeepRacer.reward import reward_pace


def plot_speed_reward():
    x_points = []
    y_points_reward_speed = []
    y_points_reward_slowness = []

    for i in np.arange(0, 4, 0.1):
        x_points.append(i)

    for x_point in x_points:
        reward = reward_pace(1, x_point)
        y_points_reward_speed.append(reward)

    for x_point in x_points:
        reward = reward_pace(0.49, x_point)
        y_points_reward_slowness.append(reward)

    plt.plot(np.array(x_points), np.array(y_points_reward_speed))
    plt.plot(np.array(x_points), np.array(y_points_reward_slowness))
    plt.title("Reward Speed Function")
    plt.xlabel("Speed")
    plt.ylabel("Reward")
    plt.show()
