def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']  # flag to indicate if the agent is on the track
    closest_waypoints = params['closest_waypoints']  # indices of the two nearest waypoints.
    distance_from_center = params['distance_from_center']  # distance in meters from the track center
    is_left_of_center = params[
        'is_left_of_center']  # Flag to indicate if the agent is on the left side to the track center or not.
    is_offtrack = params['is_offtrack']  # Boolean flag to indicate whether the agent has gone off track.
    is_reversed = params[
        'is_reversed']  # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    heading = params['heading']  # agent's yaw in degrees
    progress = params['progress']  # percentage of track completed
    speed = params['speed']  # agent's speed in meters per second (m/s)
    steering_angle = params['steering_angle']  # agent's steering angle in degrees
    steps = params['steps']  # number steps completed
    track_length = params['track_length']  # track length in meters.
    track_width = params['track_width']  # width of the track
    waypoints = params['waypoints']  # list of (x,y) as milestones along the track center

    # Calculate 3 markers that are at varying distances away from the center line

    reward = reward_distance_from_center(track_width, all_wheels_on_track, is_reversed, distance_from_center)

    reward = reward_pace(reward, speed)

    reward = reward_driving_straight(reward, steering_angle, is_left_of_center)

    return float(reward)


def reward_distance_from_center(track_width, all_wheels_on_track, is_reversed, distance_from_center):
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if not all_wheels_on_track:
        reward = 1e-2
    elif is_reversed:
        reward = 1e-2
    elif distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-2

    return reward


def reward_pace(reward, speed):
    if reward >= 0.5:
        reward = reward_speed(reward, speed)
    else:
        reward = reward_slowness(reward, speed)
    return reward


def reward_speed(reward, speed):
    if speed >= 3:
        reward = reward * 0.5
    elif speed >= 2:
        reward = reward * 1
    elif speed >= 1:
        reward = reward * 0.5
    elif speed < 1 and speed != 0:
        reward = reward * 0.25
    elif speed == 0:
        reward = reward * 0.125
    return reward


def reward_slowness(reward, speed):
    if speed >= 3:
        reward = reward * 0.125
    elif speed >= 2:
        reward = reward * 0.25
    elif speed >= 1:
        reward = reward * 0.5
    elif speed < 1 and speed != 0:
        reward = reward * 1.0
    elif speed == 0:
        reward = reward * 0.125

    return reward


def reward_driving_straight(reward, steering_angle, is_left_of_center):
    if reward >= 0.5:
        if steering_angle > 5 or steering_angle < -5:
            reward *= 0.7
    else:
        if is_left_of_center and steering_angle > 0:
            reward *= 0.7
        if not is_left_of_center and steering_angle < 0:
            reward *= 0.7
    return reward
