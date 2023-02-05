import unittest
from nose.tools import assert_equal

from DeepRacer.reward import reward_speed, reward_driving_straight

from parameterized import parameterized

parameter = {
    "all_wheels_on_track": True,
    "x": 0.0,
    "y": 0.0,
    "closest_objects": [0, 0],
    "closest_waypoints": [0, 0],
    "distance_from_center": 0.0,
    "is_crashed": False,
    "is_left_of_center": False,
    "is_offtrack": False,
    "is_reversed": False,
    "heading": float,
    "objects_distance": [],
    "objects_heading": [],
    "objects_left_of_center": [],
    "objects_location": [],
    "objects_speed": [],
    "progress": 0.0,
    "speed": 0.0,
    "steering_angle": 0.0,
    "steps": 0,
    "track_length": 0.0,
    "track_width": 0.0,
    "waypoints": []
}


class Test(unittest.TestCase):

    @parameterized.expand([  # Reward speed ->
        (1.0, 3.0, 0.5),
        (1.0, 2.0, 1),
        (1.0, 1.0, 0.5),
        (1.0, 0.9, 0.25),
        (1.0, 0, 0.125),  # edge cases ->
        (1.0, 3.1, 0.5),
        (1.0, 0.2, 0.25),
        (1.0, 2.1, 1),
        (1.0, 1.9, 0.5),  # -> reward slowness
        (0.4, 3.0, 0.05),
        (0.4, 2.0, 0.1),
        (0.4, 1.0, 0.2),
        (0.4, 0.9, 0.4),
        (0.4, 0, 0.05),  # edge cases ->
        (0.4, 3.1, 0.05),
        (0.4, 0.2, 0.4),
        (0.4, 2.1, 0.1),
        (0.4, 1.9, 0.2),  # Taking actual reward in account ->
        (0.5, 2.0, 0.5),  # Perfect speed
        (0.5, 1, 0.25),  # Ok Speed
        (0.5, 0, 0.0625)  # Too slow
    ])
    def test_reward_speed(self, reward, speed, expected_reward):
        result = reward_speed(reward, speed)
        if result != expected_reward:
            print("")
            print(
                "Speed: " + str(speed) + " expected reward: " + str(expected_reward) + " actual reward: " + str(result))
        assert_equal(expected_reward, round(result, 5))

    @parameterized.expand([  # Reward driving straight ->
        (1.0, 0.0, 1.0),
        (0.5, 0.0, 0.5),  # Not driving straight ->
        (1.0, 10, 0.7),
        (1.0, 5.1, 0.7),
        (1.0, - 5.1, 0.7),
        (0.5, 10, 0.35),  # Driving in acceptable parameters ->
        (1.0, 5, 1.0),
        (1.0, - 5, 1.0)
    ])
    def test_reward_driving_straight(self, reward, steering_angle, expected_reward):
        result = reward_driving_straight(reward, steering_angle, False)
        assert_equal(result, expected_reward)

    #  + straight -> right | - straight -> left

    @parameterized.expand([  # Reward driving not straight ->
        (0.4, - 10.0, True, 0.4),
        (0.4, 10.0, True, 0.28),
        (0.4, 10.0, False, 0.4),
        (0.4, - 10.0, False, 0.28),
    ])
    def test_reward_driving_not_straight(self, reward, steering_angle, is_left_of_center, expected_reward):
        result = reward_driving_straight(reward, steering_angle, is_left_of_center)
        assert_equal(expected_reward, round(result, 5))
