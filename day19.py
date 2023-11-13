#! /usr/bin/env python3
import re
import sys
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Blueprint:
    name: int
    ore_robot_cost: int
    clay_robot_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int


@dataclass
class State:
    ore: int
    clay: int
    obsidian: int
    geodes: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int


if __name__ == "__main__":
    blueprints: "list[Blueprint]" = []

    for line in sys.argv[1].split("\n\n"):
        nums = re.findall(r"\d+", line)
        blueprints.append(Blueprint(*nums))
    pprint(blueprints)
