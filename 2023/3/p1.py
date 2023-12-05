import re

total_sum = 0

matrix = []

lines = []

len_line = None

# Open input file
with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
        line = line.strip()
        if len_line is None:
            len_line = len(line)
        assert len(line) == len_line
        lines.append(line)
        matrix.append([])
        for c in line:
            matrix[i].append(c)

[
    print(f"{x.group()}, {x.start(0)}, {x.end(0)}")
    for x in re.finditer(r"(\d+)", "467..114..")
]


def is_near_symbol(start: int, end: int, col: int):
    print(f"start: {start}, end: {end}, col: {col}")
    for i in range(max(start - 1, 0), min(end + 1, len(matrix[col]))):
        for j in range(max(0, col - 1), min(len(matrix), col + 2)):
            if not re.match(r"\d|\.", matrix[j][i]):
                # Found a symbol
                assert not matrix[j][i].isdigit()
                assert matrix[j][i] != "."
                print(f"Symbol: {matrix[j][i]}")
                return True
    return False


# Read file
for i, line in enumerate(lines):
    # if i > 3:
    #     break
    print(i)
    print(line)
    numbers = re.finditer(r"(\d+)", line)
    for num in numbers:
        print(f"num: {int(num.group())}")
        if is_near_symbol(num.start(0), num.end(0), i):
            print("FOUND")
            total_sum += int(num.group())


print(f"Total sum: {total_sum}")
