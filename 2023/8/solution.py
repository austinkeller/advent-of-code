from dataclasses import dataclass
from math import lcm


@dataclass
class Node:
    name: str
    children: list[str]

    @staticmethod
    def parse_from_line(line: str) -> "Node":
        line = line.strip()
        name, children = (x.strip() for x in line.split("="))
        children = children.strip("() ")
        children = [x.strip(" ") for x in children.split(",")]
        return Node(name, children)


assert Node.parse_from_line("BBB = (DDD, EEE)").name == "BBB"
assert Node.parse_from_line("BBB = (DDD, EEE)").children[0] == "DDD"
assert Node.parse_from_line("BBB = (DDD, EEE)").children[1] == "EEE"


@dataclass
class InstructionMap:
    node_map: dict[str, Node]
    lr_instructions: str

    @staticmethod
    def read_from_file() -> "InstructionMap":
        node_map: dict[str, Node] = {}

        # Open input file
        with open(0) as f:
            # Read file
            lr_instructions = f.readline().strip()
            f.readline()
            for line in f.readlines():
                node = Node.parse_from_line(line)
                node_map[node.name] = node
        return InstructionMap(node_map, lr_instructions)


@dataclass
class CycleInfo:
    steps_to_cycle: int
    steps_for_z_nodes: dict[str, int]
    step_of_first_repeated_state: int
    cycle_size: int


def find_distance_to_cycle_and_z_indices(
    node: Node, node_map, lr_instructions
) -> CycleInfo:
    states_seen_to_step: dict[tuple[str, int], int] = {}
    step = 0
    z_steps = {}
    while True:
        for i, d in enumerate(lr_instructions):
            node = node_map[node.children[0 if d == "L" else 1]]
            step += 1
            if (node.name, i) in states_seen_to_step:
                # Found cycle
                return CycleInfo(
                    step,
                    z_steps,
                    states_seen_to_step[(node.name, i)],
                    step - states_seen_to_step[(node.name, i)],
                )
            states_seen_to_step[(node.name, i)] = step
            if node.name.endswith("Z") and node.name not in z_steps:
                z_steps[node.name] = step


if __name__ == "__main__":
    instruction_map = InstructionMap.read_from_file()
    node_map, lr_instructions = (
        instruction_map.node_map,
        instruction_map.lr_instructions,
    )

    # Part 1
    if "AAA" in node_map:
        node = node_map["AAA"]
        step = 0
        while node.name != "ZZZ":
            for d in lr_instructions:
                if node.name == "ZZZ":
                    break
                i = 0 if d == "L" else 1
                node = node_map[node.children[i]]
                step += 1
        print(f"Steps to reach ZZZ: {step}")

    # Part 2
    nodes = []
    step = 0
    for name in node_map.keys():
        if name.endswith("A"):
            nodes.append(node_map[name])

    cycles = []

    for node in nodes:
        cycle_info = find_distance_to_cycle_and_z_indices(
            node, node_map, lr_instructions
        )
        print(cycle_info)
        cycles.append(cycle_info)

    print(f"Steps to reach all **Zs: {lcm(*[x.cycle_size for x in cycles])}")
