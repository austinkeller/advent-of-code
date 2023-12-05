import re

total_sum = 0

lines: list[str] = []

# Open input file
with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
        line = line.strip()
        lines.append(line)


# Read file
for line_num, line in enumerate(lines):
    symbols = re.finditer(r"(\*)", line)
    for symbol in symbols:
        numbers = []
        # Find digits
        for i in range(line_num - 1, line_num + 2):
            if i < 0 or i >= len(lines):
                continue
            for j in range(symbol.start(0) - 1, symbol.end(0) + 1):
                if j < 0 or j >= len(line):
                    continue
                if lines[i][j].isdigit():
                    if any(
                        [
                            number["start"] <= j
                            and number["end"] > j
                            and i == number["row"]
                            for number in numbers
                        ]
                    ):
                        # already saw number
                        continue
                    # Found number, extract it
                    low = j
                    while low > 0 and lines[i][low - 1].isdigit():
                        low -= 1
                    high = j
                    while high < len(line) and lines[i][high].isdigit():
                        high += 1
                    numbers.append(
                        {
                            "value": int(lines[i][low:high]),
                            "start": low,
                            "end": high,
                            "row": i,
                        }
                    )
        if len(numbers) == 2:
            # Found a gear
            total_sum += numbers[1]["value"] * numbers[0]["value"]


print(f"Total sum: {total_sum}")
