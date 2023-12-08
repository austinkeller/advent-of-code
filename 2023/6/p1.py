import math
from functools import reduce


def parse_line(line: str) -> list[int]:
    _, *vals = filter(lambda x: x != "", line.strip().split(" "))
    vals = list(map(int, vals))
    return vals


def quadratic_formula(a, b, c) -> tuple[int, int]:
    part = math.sqrt(b**2 - 4 * a * c)
    # part = int(round(part))
    # print(part)
    solutions = sorted([(-b + part) / (2 * a), (-b - part) / (2 * a)])
    print(solutions)
    return (math.floor(solutions[0] + 1), math.ceil(solutions[1] - 1))


def find_record_times(time: int, distance: int) -> range:
    """
    distance = x * (time - x)
    distance = time * x - x**2


    0 = -x**2 + time * x - distance
    0 = x**2 - time * x + distance
    0 = x**2 - time * x + distance


    """
    solutions = quadratic_formula(1, -time, distance)
    print(solutions)
    return range(solutions[0], solutions[1] + 1)


assert range(2, 6) == find_record_times(7, 9), find_record_times(7, 9)
assert range(4, 12) == find_record_times(15, 40)
assert range(11, 20) == find_record_times(30, 200), find_record_times(30, 200)


if __name__ == "__main__":
    # Open input file
    with open(0) as f:
        # Read file
        times = parse_line(f.readline())
        distances = parse_line(f.readline())
        print(times)
        print(distances)
    record_counts = []
    for time, distance in list(zip(times, distances)):
        record_counts.append(len(find_record_times(time, distance)))
    print(reduce(lambda x, y: x * y, record_counts, 1))

    time = int(reduce(lambda x, y: x + y, map(str, times)))
    distance = int(reduce(lambda x, y: x + y, map(str, distances)))
    print(len(find_record_times(time, distance)))
