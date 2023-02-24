import matplotlib.pyplot as plt
import numpy as np

from DeepRacer.reward import reward_speed


def plot_speed_reward():
    x_points = []
    y_points = []

    for i in np.arange(0, 4, 0.1):
        x_points.append(i)
        print(i)

    print(x_points)

    for x_point in x_points:
        reward = reward_speed(1, x_point)
        y_points.append(reward)

    plt.plot(np.array(x_points), np.array(y_points))
    plt.title("Reward Speed Function")
    plt.xlabel("Speed")
    plt.ylabel("Reward")
    plt.show()
