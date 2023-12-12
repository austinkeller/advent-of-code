from math import ceil
from collections import deque

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

DIRECTIONS = [LEFT, UP, RIGHT, DOWN]

DIRECTION_NAMES = {
    LEFT: "LEFT",
    RIGHT: "RIGHT",
    UP: "UP",
    DOWN: "DOWN",
}

PIPE_TO_DIRECTIONS = {
    "7": [LEFT, DOWN],
    "J": [UP, LEFT],
    "L": [RIGHT, UP],
    "F": [DOWN, RIGHT],
    "-": [LEFT, RIGHT],
    "|": [UP, DOWN],
    ".": [],
}

PIPE_TO_ROTATION = {
    "7": 90,
    "J": 90,
    "L": 90,
    "F": 90,
    "-": 0,
    "|": 0,
}


def reverse_direction(d: tuple[int, int]) -> tuple[int, int]:
    return -d[0], -d[1]


def step_direction(
    position: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    return position[0] + direction[0], position[1] + direction[1]


def rotate_direction(direction, degrees) -> tuple[int, int]:
    offset = int(degrees // 90)
    start = DIRECTIONS.index(direction)
    try:
        return DIRECTIONS[(start + offset) % len(DIRECTIONS)]
    except IndexError:
        print(f"start: {start}, offset: {offset}")
        raise


assert rotate_direction(LEFT, 90) == UP
assert rotate_direction(LEFT, -90) == DOWN
assert rotate_direction(UP, 90) == RIGHT
assert rotate_direction(UP, 180) == DOWN
assert rotate_direction(UP, 540) == DOWN


class ColorSketch:
    def __init__(self, height, width):
        self.color_sketch = []
        for i in range(height):
            self.color_sketch.append([])
            for j in range(width):
                self.color_sketch[-1].append("_")

    def get_color(self, position):
        return self.color_sketch[position[0]][position[1]]

    def is_marked(self, position):
        return self.color_sketch[position[0]][position[1]] != "_"

    def mark_position(self, position):
        self.set_color(position, "X")

    def set_color(self, position, value):
        self.color_sketch[position[0]][position[1]] = value

    def __repr__(self):
        return "\n".join(["".join(line) for line in self.color_sketch])

    def has_position(self, position):
        return 0 <= position[0] < len(self.color_sketch) and 0 <= position[1] < len(
            self.color_sketch[0]
        )


if __name__ == "__main__":
    sketch: list[str] = []
    # Color a map of all places previously visited
    color_sketch: ColorSketch

    directions_history = []
    positions_history = []
    start_position = None
    # Open input file
    with open(0) as f:
        # Read file
        for i, line in enumerate(f.readlines()):
            sketch.append(line.strip())
            if "S" in sketch[i]:
                j = sketch[i].index("S")
                assert start_position is None
                start_position = i, j

    color_sketch = ColorSketch(len(sketch), len(sketch[0]))
    color_sketch.mark_position(start_position)

    assert start_position is not None

    def get_rotation_for_position(position, prev_direction) -> int:
        return get_rotation_for_pipe(character_at_position(position), prev_direction)

    def get_rotation_for_pipe(pipe, prev_direction) -> int:
        if pipe == "S":
            return 0
        rotation_sign = (
            1
            if PIPE_TO_DIRECTIONS[pipe].index(reverse_direction(prev_direction)) == 0
            else -1
        )
        return rotation_sign * PIPE_TO_ROTATION[pipe]

    def character_at_position(position: tuple[int, int]) -> str:
        return sketch[position[0]][position[1]]

    def find_connected_pipe_at_position(
        position: tuple[int, int]
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        # Search around for a connected pipe
        connected_positions = []
        directions = []
        for search_d in [LEFT, UP, RIGHT, DOWN]:
            try_position = step_direction(position, search_d)
            c = character_at_position(try_position)
            for pipe_d in PIPE_TO_DIRECTIONS[c]:
                if search_d == reverse_direction(pipe_d):
                    connected_positions.append(try_position)
                    directions.append(search_d)
        return connected_positions, directions

    def get_next_direction_for_position(position, prev_direction) -> tuple[int, int]:
        available_directions = PIPE_TO_DIRECTIONS[character_at_position(position)]
        return list(
            filter(
                lambda d: d != reverse_direction(prev_direction), available_directions
            )
        )[0]

    # Search around for a connected pipe
    initial_next_positions, initial_directions = find_connected_pipe_at_position(
        start_position
    )

    # Infer start pipe type
    start_pipe = list(
        filter(
            lambda x: x is not None,
            [
                pipe if set(directions) == set(initial_directions) else None
                for pipe, directions in PIPE_TO_DIRECTIONS.items()
            ],
        )
    )[0]

    print(f"Inferred start pipe: {start_pipe}")

    # Arbitrarily pick a direction
    position, prev_direction = initial_next_positions[0], initial_directions[0]
    total_rotation = get_rotation_for_pipe(
        start_pipe, reverse_direction(initial_directions[1])
    )
    print(
        f"Starting by turning {total_rotation}, stepping {DIRECTION_NAMES[prev_direction]} to {character_at_position(position)}"
    )

    current_pipe = character_at_position(position)
    steps = 1

    directions_history.append(prev_direction)
    positions_history.append(start_position)

    while current_pipe != "S":
        color_sketch.mark_position(position)
        rotation = get_rotation_for_position(position, prev_direction)
        next_direction = get_next_direction_for_position(position, prev_direction)
        positions_history.append(position)
        directions_history.append(next_direction)
        position = step_direction(position, next_direction)
        prev_direction = next_direction

        current_pipe = character_at_position(position)
        print(
            f"Turn {rotation}, step {DIRECTION_NAMES[prev_direction]} to {current_pipe}"
        )
        steps += 1
        total_rotation += rotation

    positions_history.append(position)
    directions_history.append(next_direction)

    print(f"Part 1: Distance halfway around the loop: {ceil(steps / 2)}")
    print(f"Total rotation: {total_rotation}")

    spin = 1 if total_rotation == 360 else -1
    inside_normal_direction = rotate_direction(initial_directions[0], 90 * spin)

    print(color_sketch)

    def search_inside(position, inside_normal_direction) -> int:
        queue = deque()
        queue.append((position, inside_normal_direction))
        tile_count = 0
        while queue:
            p, d = queue.pop()
            next_position = step_direction(p, d)
            if not color_sketch.has_position(next_position) or color_sketch.is_marked(
                next_position
            ):
                continue
            color_sketch.set_color(next_position, "+")
            print(f"Marking {next_position}")
            tile_count += 1
            for try_d in DIRECTIONS:
                # if try_d == reverse_direction(d):
                #     continue
                queue.append((next_position, try_d))
        if tile_count > 0:
            print(color_sketch)
        return tile_count

    # Search the map in the direction of the inside direction, coloring and adding to total
    tile_count = 0
    for position, direction in zip(positions_history, directions_history):
        inside_normal_direction = rotate_direction(direction, spin * 90)
        print(
            f"{character_at_position(position)}, stepping {DIRECTION_NAMES[direction]}, normal is {DIRECTION_NAMES[inside_normal_direction]}"
        )
        tile_count += search_inside(position, inside_normal_direction)

    # Report total inside tiles colored
    # TODO Why is this giving 392 and not 393???
    print(f"Part 2: Tile count: {tile_count}")
