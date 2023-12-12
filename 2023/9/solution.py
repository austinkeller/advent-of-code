def diff(V: list[int]) -> list[int]:
    if len(V) <= 1:
        return []
    return [V[i] - V[i - 1] for i in range(1, len(V))]


def extrapolate_forward(histories: list[list[int]]):
    extrapolates = []

    for history in histories:
        derivatives = [history]
        while derivatives[-1] and not all(x == 0 for x in derivatives[-1]):
            derivatives.append(diff(derivatives[-1]))
        # Now extrapolate
        extrapolate = 0
        for i in reversed(range(len(derivatives))):
            extrapolate = derivatives[i][-1] + extrapolate
        extrapolates.append(extrapolate)
    print(f"Sum of extrapolated values is {sum(extrapolates)}")


def extrapolate_backward(histories: list[list[int]]):
    extrapolates = []

    for history in histories:
        # print(f"History: {history}")
        derivatives = [history]
        while derivatives[-1] and not all(x == 0 for x in derivatives[-1]):
            derivatives.append(diff(derivatives[-1]))
        # Now extrapolate
        extrapolate = 0
        for i in reversed(range(len(derivatives))):
            # print(f"i: {i} {derivatives[i]}")
            extrapolate = derivatives[i][0] - extrapolate
        extrapolates.append(extrapolate)
    # print(extrapolates)
    print(f"Sum of backward extrapolated values is {sum(extrapolates)}")


if __name__ == "__main__":
    histories = []
    # Open input file
    with open(0) as f:
        # Read file
        for line in f.readlines():
            history = [int(x.strip()) for x in line.strip().split(" ")]
            histories.append(history)

    extrapolate_forward(histories)
    extrapolate_backward(histories)
