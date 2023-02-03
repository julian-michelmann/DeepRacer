import unittest
from nose.tools import assert_equal

from DeepRacer.reward import reward_speed, reward_slowness

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

    # Speed -> Reward
    # 3 >= -> 1
    # 2 >= -> 0.5
    # 1 >= -> 0.25
    # 1 < -> 0.125

    @parameterized.expand([
        (3.0, 0.5),
        (2.0, 1),
        (1.0, 0.5),
        (0.9, 0.25),
        (0, 0.125),  # edge cases ->
        (3.1, 0.5),
        (0.2, 0.25),
        (2.1, 1),
        (1.9, 0.5)
    ])
    def test_reward_speed(self, speed, expected_reward):
        result = reward_speed(speed, 1)
        if result != expected_reward:
            print("")
            print(
                "Speed: " + str(speed) + " expected reward: " + str(expected_reward) + " actual reward: " + str(result))

        assert_equal(expected_reward, result)

    # Speed -> Reward
    # 3 >= -> 0.125
    # 2 >= -> 0.25
    # 1 >= -> 0.5
    # 1 < && != 0 -> 1
    # 0 == -> 0.125

    @parameterized.expand([
        (3.0, 0.125),
        (2.0, 0.25),
        (1.0, 0.5),
        (0.9, 1),
        (0, 0.125),  # edge cases ->
        (3.1, 0.125),
        (0.2, 1),
        (2.1, 0.25),
        (1.9, 0.5)
    ])
    def test_reward_slowness(self, speed, expected_reward):
        result = reward_slowness(speed, 1)
        if result != expected_reward:
            print("")
            print(
                "Speed: " + str(speed) + " expected reward: " + str(expected_reward) + " actual reward: " + str(result))
        assert_equal(expected_reward, round(result, 5))

    # reward/reward_for_speed
    @parameterized.expand([
        (0.9, 0.5, 0.5),  # Prefect speed
        (1, 0.5, 0.25),  # Ok speed
        (3, 0.5, 0.0625)  # Too fast
    ])
    def test_reward_slowness_taking_current_reward_in_account(self, speed, reward, expected_reward):
        result = reward_slowness(speed, reward)
        if result != expected_reward:
            print("")
            print(
                "Speed: " + str(speed) + " expected reward: " + str(expected_reward) + " actual reward: " + str(result))
        assert_equal(expected_reward, round(result, 5))

    # reward/reward_for_speed
    @parameterized.expand([
        (2.0, 0.5, 0.5),  # Perfect speed
        (1, 0.5, 0.25),  # Ok Speed
        (0, 0.5, 0.0625)  # Too slow
    ])
    def test_reward_speed_taking_current_reward_in_account(self, speed, reward, expected_reward):
        result = reward_speed(speed, reward)
        if result != expected_reward:
            print("")
            print(
                "Speed: " + str(speed) + " expected reward: " + str(expected_reward) + " actual reward: " + str(result))
        assert_equal(expected_reward, round(result, 5))
