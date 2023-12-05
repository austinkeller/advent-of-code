import re

total_sum = 0

m = []

# Open input file
with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
        m.append([])
        for c in line:
            m[i].append(c)

print(re.findall('(/d+)', "467..114.."))

with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
        numbers = re.findall('(/d+)', line)
        numbers


print(f"Total sum: {total_sum}")
