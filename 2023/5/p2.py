seed_ranges = []

mappers = {}


class Mapper:
    def __init__(self, source_key, dest_key):
        self.source_key = source_key
        self.dest_key = dest_key
        self.maps = []

    def add_map(self, source_start, dest_start, range_):
        self.maps.append((source_start, dest_start, range_))
        # keep maps sorted by source_start
        self.maps.sort(key=lambda x: x[0])

    def get(self, source):
        s = int(source)
        for m in self.maps:
            source_start, dest_start, range_ = m
            if s >= source_start and s < source_start + range_:
                return dest_start + s - source_start
        return s

    def reverse_get(self, dest):
        d = int(dest)
        for m in self.maps:
            source_start, dest_start, range_ = m
            if d >= dest_start and d < dest_start + range_:
                return source_start + d - dest_start
        return d

    def __getitem__(self, source):
        return self.get(source)


def join_mappers(mapper1: Mapper, mapper2: Mapper):
    assert mapper1.dest_key == mapper2.source_key
    source_key = mapper1.source_key
    dest_key = mapper2.dest_key
    mapper = Mapper(source_key, dest_key)
    # Combine all dest keys of mapper1 with source keys of mapper 2 into new set of keys
    intermediate_keys = set()
    for m in mapper1.maps:
        source_start, dest_start, range_ = m
        intermediate_keys.add(dest_start)
        intermediate_keys.add(dest_start + range_)
    for m in mapper2.maps:
        source_start, dest_start, range_ = m
        intermediate_keys.add(source_start)
        intermediate_keys.add(source_start + range_)
    intermediate_keys = list(sorted(intermediate_keys))

    # Create new boundaries from the mapper1 source of the intermediate keys to the mapper2 dest of the intermediate keys
    boundaries = []
    for i_key in intermediate_keys:
        boundaries.append((mapper1.reverse_get(i_key), mapper2.get(i_key)))

    boundaries = list(sorted(boundaries))

    # Create new maps from the boundaries
    for i in range(len(boundaries) - 1):
        source_start, dest_start = boundaries[i]
        source_end, dest_end = boundaries[i + 1]
        mapper.add_map(source_start, dest_start, source_end - source_start)
    return mapper


# Open input file
with open(0) as f:
    # Read file
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip()

        if line.startswith("seeds:"):
            seeds = line.split(":")[1].strip().split(" ")
            # Filter out empty strings
            seeds = list(filter(None, seeds))
            seeds = [int(x) for x in seeds]
            assert len(seeds) % 2 == 0
            for i in range(0, len(seeds), 2):
                seed_ranges.append((seeds[i], seeds[i + 1]))
        elif line.endswith(" map:"):
            source_key, _, dest_key = line.split(" ")[0].split("-")
            if source_key not in mappers:
                mappers[source_key] = Mapper(source_key, dest_key)
            while True:
                line = f.readline().strip()
                if line == "":
                    break
                dest_start, source_start, range_ = [x.strip() for x in line.split(" ")]
                source_start = int(source_start)
                dest_start = int(dest_start)
                range_ = int(range_)
                mappers[source_key].add_map(source_start, dest_start, range_)


# Join mappers
total_mapper = mappers["seed"]
while total_mapper.dest_key != "location":
    total_mapper = join_mappers(total_mapper, mappers[total_mapper.dest_key])

# print(f"total_mapper.maps: {total_mapper.maps}")
# print("")

# print(f"seed_ranges: {seed_ranges}")
# print("")

# Break all seed ranges that span multiple mapper source ranges into non-overlapping seed ranges
new_seed_ranges = []
for start_seed, seed_range in seed_ranges:
    new_seed_ranges_for_seed_range = []
    # Split seed range anywhere a mapper source range boundary is crossed
    for m in total_mapper.maps:
        source_start, _, range_ = m
        # print(f"start_seed: {start_seed}, seed_range: {seed_range}, source_start: {source_start}, source_end: {source_start + range_}")
        if source_start > start_seed and source_start < start_seed + seed_range - 1:
            # Split seed range
            # print(f"Split seed range on source start: {start_seed}, {source_start - start_seed}")
            new_seed_ranges_for_seed_range.append(
                (start_seed, source_start - start_seed)
            )
            seed_range -= source_start - start_seed
            start_seed = source_start
        if (
            source_start + range_ > start_seed
            and source_start + range_ < start_seed + seed_range - 1
        ):
            # Split seed range
            # print(f"Split seed range on source end: {start_seed}, {source_start + range_ - start_seed}")
            new_seed_ranges_for_seed_range.append(
                (start_seed, source_start + range_ - start_seed)
            )
            seed_range -= source_start + range_ - start_seed
            start_seed = source_start + range_

    new_seed_ranges_for_seed_range.append((start_seed, seed_range))
    new_seed_ranges.extend(new_seed_ranges_for_seed_range)

# print(f"new_seed_ranges: {new_seed_ranges}")
# print("")

# Now map the seed ranges to location ranges, pick the minimum location, and then reverse map to get the seed
min_location = None
for start_seed, seed_range in new_seed_ranges:
    start_location = total_mapper[start_seed]
    # print(f"start_seed: {start_seed}, seed_range: {seed_range}, start_location: {start_location}")
    if min_location is None or start_location < min_location:
        min_location = start_location

print(f"Min seed: {total_mapper.reverse_get(min_location)}")
print(f"Min location: {min_location}")
