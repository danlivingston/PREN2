import json
from heapq import heappop, heappush

from cubepiler import motor_control
from loguru import logger


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

    exit_counter = 0
    while exit_counter < 9:  # should be done after 8 max since only 8 cubes fit
        exit_counter += 1

        queue = []
        logger.trace(f"starting new calculation loop; current action queue {actions}")

        for i in range(4):
            tbp = to_be_placed[i]
            if not tbp == None:
                color_wanted = cube_plan[tbp]

                slot_index = (tbp * 3) % 12

                if color_wanted == 0:
                    logger.trace(f"no cube{" ":<6}at pos {tbp} ({slot_index});")
                    to_be_placed[i] = None

                else:
                    color_shaft_pos = shaft_colors.index(color_wanted)

                    shaft_index = (color_shaft_pos * 4 + pos) % 12
                    distance = (slot_index - shaft_index) % 12

                    heappush(queue, (distance, tbp))

                    logger.trace(
                        f"color {reverse_map_color(color_wanted):^6} at pos {tbp} ({slot_index}); shaft currently at {shaft_index}; distance between: {distance}"
                    )

        if len(queue) == 0:
            return actions

        next = heappop(queue)
        move, drop = next
        actions.append((move, drop % 4))

        logger.trace(
            f"best move chosen as rotate by {move} ({int(move/12*360):>3}°); drop shaft {(drop%4)+1}"
        )

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


if __name__ == "__main__":

    import testdata

    place_cubes(testdata.config01)
    place_cubes(testdata.config02)
    place_cubes(testdata.config03)
