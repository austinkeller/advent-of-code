seeds = []

mappers = {}


class Mapper:
    def __init__(self, source_key, dest_key):
        self.source_key = source_key
        self.dest_key = dest_key
        self.maps = []

    def add_map(self, source_start, dest_start, range_):
        self.maps.append((source_start, dest_start, range_))

    def get(self, source):
        s = int(source)
        for m in self.maps:
            source_start, dest_start, range_ = m
            if s >= source_start and s < source_start + range_:
                return dest_start + s - source_start
        return s

    def __getitem__(self, source):
        return self.get(source)


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


locations = []
for seed in seeds:
    key = 'seed'
    while key != 'location':
        print(f"{key}: {seed}")
        mapper = mappers[key]
        seed = mapper[seed]
        key = mapper.dest_key
    print(f"{key}: {seed}")
    locations.append(seed)

print(min(locations))
