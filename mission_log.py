mission_counter = 1

mission_history = set()


def set_counter(value):

    global mission_counter

    mission_counter = value


def get_counter():

    return mission_counter


def increment_counter():

    global mission_counter

    mission_counter += 1


def clear_history():

    mission_history.clear()


def mission_exists(mission):

    return mission in mission_history


def add_mission(mission):

    mission_history.add(mission)
