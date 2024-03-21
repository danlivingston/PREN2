import json
from heapq import heappop, heappush
from loguru import logger


import motor_control


def get_cube_placing_actions(input):
    input = json.loads(input)
    cube_color_map = {"": 0, "red": 1, "yellow": 2, "blue": 3}
    cube_plan = [0, 0, 0, 0, 0, 0, 0, 0]
    to_be_placed = [0, 1, 2, 3]  # indexes for ^
    shaft_colors = ["red", "yellow", "blue"]

    # print("colors in shaft", shaft_colors)
    logger.debug(
        f"colors in shaft A:{shaft_colors[0]} B:{shaft_colors[1]} C:{shaft_colors[2]}"
    )

    queue = []  # heappush(self._queue, (10, "item_with_priority_10"))
    pos = 0  # position of _shaft_colors[0]

    def map_color(name):
        return cube_color_map[name]

    def reverse_map_color(color):
        reverse_cube_color_map = {v: k for k, v in cube_color_map.items()}
        return reverse_cube_color_map[color]

    config = input["config"]
    cube_plan = list(map(lambda x: map_color(x[1]), config.items()))
    shaft_colors = list(map(map_color, shaft_colors))

    logger.debug(f"planning to place {list(map(reverse_map_color,cube_plan))}")

    actions = []

    debug_last_resort_exit_counter = 0
    while (
        debug_last_resort_exit_counter < 9
    ):  # should be done after 8 max since only 8 cubes fit
        debug_last_resort_exit_counter += 1

        # print("=-= NEW LOOP =-=")
        # print(moves)

        queue = []
        logger.debug(f"starting new calculation loop; current action queue {actions}")

        for i in range(4):
            tbp = to_be_placed[i]
            if not tbp == None:
                color_wanted = cube_plan[tbp]

                slot_index = (tbp * 3) % 12

                if color_wanted == 0:
                    logger.debug(f"no cube{" ":<6}at pos {tbp} ({slot_index});")
                    to_be_placed[i] = None

                else:
                    color_shaft_pos = shaft_colors.index(color_wanted)

                    shaft_index = (color_shaft_pos * 4 + pos) % 12
                    distance = (slot_index - shaft_index) % 12

                    heappush(queue, (distance, tbp))

                    # print(
                    #     "color",
                    #     color_wanted,
                    #     "at",
                    #     slot_index,
                    #     "; shaft at",
                    #     shaft_index,
                    #     "; distance",
                    #     distance,
                    #     "; queue",
                    #     queue,
                    # )

                    logger.debug(
                        f"color {reverse_map_color(color_wanted):^6} at pos {tbp} ({slot_index}); shaft currently at {shaft_index}; distance between: {distance}"
                    )

        if len(queue) == 0:
            return actions

        next = heappop(queue)
        move, drop = next
        actions.append((move, drop % 4))

        # print(
        #     "rotate by", move, "drop shaft", drop % 4, "dropped color", cube_plan[drop]
        # )
        
        logger.debug(f"best move chosen as move by {move} ({int(move/12*360):>3}°)")

        if drop < 4:
            to_be_placed[drop] = to_be_placed[drop] + 4
        else:
            to_be_placed[drop % 4] = None

        pos = (pos + move) % 12


def place_cubes(input):
    logger.info("starting cube placement")
    actions = get_cube_placing_actions(input)
    logger.info("calculated actions")
    logger.info("starting placement")
    motor_control.execute_actions(actions)
    logger.success("completed cube placement")


test_config01 = """{
  "time": "2023-10-10 17:10:05",
  "config": {
    "1": "red",
    "2": "blue",
    "3": "red",
    "4": "yellow",
    "5": "",
    "6": "",
    "7": "yellow",
    "8": "red"
  }
}"""

test_config02 = """{
  "time": "2023-11-15 21:09:05",
  "config": {
    "1": "yellow",
    "2": "red",
    "3": "",
    "4": "blue",
    "5": "yellow",
    "6": "red",
    "7": "",
    "8": "blue"
  }
}"""

test_config03 = """{
  "time": "2023-11-15 21:09:05",
  "config": {
    "1": "blue",
    "2": "blue",
    "3": "yellow",
    "4": "red",
    "5": "red",
    "6": "red",
    "7": "blue",
    "8": "yellow"
  }
}"""

place_cubes(test_config01)

# class bcolors:
#     HEADER = "\033[95m"
#     OKBLUE = "\033[94m"
#     OKGREEN = "\033[92m"
#     WARNING = "\033[93m"
#     FAIL = "\033[91m"
#     ENDC = "\033[0m"
#     BOLD = "\033[1m"
#     UNDERLINE = "\033[4m"


# def calc_total_moves_debug(placement):
#     d = 0
#     for move in placement:
#         d += move[0]
#     return d


# actions = get_cube_placing_actions(test_config01)
# d = calc_total_moves_debug(actions)
# print(bcolors.OKBLUE, test_config01, bcolors.ENDC)
# print(bcolors.OKGREEN, actions, bcolors.ENDC)
# motor_control.execute_actions(actions)
# print(
#     bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE,
#     "total distance",
#     d,
#     "->",
#     round(d / 12, 2),
#     "rotations ->",
#     int(d / 12 * 360),
#     "degrees",
#     bcolors.ENDC,
# )
# print()


# actions = get_cube_placing_actions(test_config02)
# d = calc_total_moves_debug(actions)
# print(bcolors.OKBLUE, test_config02, bcolors.ENDC)
# print(bcolors.OKGREEN, actions, bcolors.ENDC)
# motor_control.execute_actions(actions)
# print(
#     bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE,
#     "total distance",
#     d,
#     "->",
#     round(d / 12, 2),
#     "rotations ->",
#     int(d / 12 * 360),
#     "degrees",
#     bcolors.ENDC,
# )
# print()

# actions = get_cube_placing_actions(test_config03)
# d = calc_total_moves_debug(actions)
# print(bcolors.OKBLUE, test_config03, bcolors.ENDC)
# print(bcolors.OKGREEN, actions, bcolors.ENDC)
# motor_control.execute_actions(actions)
# print(
#     bcolors.BOLD + bcolors.HEADER + bcolors.UNDERLINE,
#     "total distance",
#     d,
#     "->",
#     round(d / 12, 2),
#     "rotations ->",
#     int(d / 12 * 360),
#     "degrees",
#     bcolors.ENDC,
# )
# print()
