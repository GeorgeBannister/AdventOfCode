#! /usr/bin/env python3
import re
import sys
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Blueprint:
    name: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int


@dataclass(frozen=True)
class State:
    ore: int
    clay: int
    obsidian: int
    geodes: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int

    def post_buy_ore_robot(self, blueprint: Blueprint):
        return State(
            self.ore - blueprint.ore_robot_ore_cost,
            self.clay,
            self.obsidian,
            self.geodes,
            self.ore_robots + 1,
            self.clay_robots,
            self.obsidian_robots,
            self.geode_robots,
        )

    def post_buy_clay_robot(self, blueprint: Blueprint):
        return State(
            self.ore - blueprint.clay_robot_ore_cost,
            self.clay,
            self.obsidian,
            self.geodes,
            self.ore_robots,
            self.clay_robots + 1,
            self.obsidian_robots,
            self.geode_robots,
        )

    def post_buy_obsidian_robot(self, blueprint: Blueprint):
        return State(
            self.ore - blueprint.obsidian_robot_ore_cost,
            self.clay - blueprint.obsidian_robot_clay_cost,
            self.obsidian,
            self.geodes,
            self.ore_robots,
            self.clay_robots,
            self.obsidian_robots + 1,
            self.geode_robots,
        )

    def post_buy_geode_robot(self, blueprint: Blueprint):
        return State(
            self.ore - blueprint.geode_robot_ore_cost,
            self.clay,
            self.obsidian - blueprint.geode_robot_obsidian_cost,
            self.geodes,
            self.ore_robots,
            self.clay_robots,
            self.obsidian_robots,
            self.geode_robots + 1,
        )

    def after_mining(self, blueprint: Blueprint):
        return State(
            self.ore + self.ore_robots,
            self.clay + self.clay_robots,
            self.obsidian + self.obsidian_robots,
            self.geodes + self.geode_robots,
            self.ore_robots,
            self.clay_robots,
            self.obsidian_robots,
            self.geode_robots,
        )


@dataclass
class StateAllowedToBuy:
    state: State
    ore_robot_valid: bool
    clay_robot_valid: bool
    obsidian_robot_valid: bool


def rec_run_turn(
    state_allowed: StateAllowedToBuy,
    blueprint: Blueprint,
    turn: int,
    state_history: dict,
    end_turn: int,
) -> int:
    state = state_allowed.state
    if turn == end_turn:
        return state.geodes
    options: list[state_allowed] = []

    can_buy_geode_robot = (
        state.ore >= blueprint.geode_robot_ore_cost
        and state.obsidian >= blueprint.geode_robot_obsidian_cost
    )

    can_buy_ore_robot = (
        not can_buy_geode_robot
        and state.ore >= blueprint.ore_robot_ore_cost
        and state_allowed.ore_robot_valid
        and not (
            state.ore_robots
            >= max(
                blueprint.clay_robot_ore_cost,
                blueprint.obsidian_robot_ore_cost,
                blueprint.geode_robot_ore_cost,
            )
        )
    )
    can_buy_clay_robot = (
        not can_buy_geode_robot
        and state.ore >= blueprint.clay_robot_ore_cost
        and state_allowed.clay_robot_valid
        and not (state.clay_robots >= blueprint.obsidian_robot_clay_cost)
    )
    can_buy_obsidian_robot = (
        not can_buy_geode_robot
        and state.ore >= blueprint.obsidian_robot_ore_cost
        and state.clay >= blueprint.obsidian_robot_clay_cost
        and state_allowed.obsidian_robot_valid
        and not (state.obsidian_robots >= blueprint.geode_robot_obsidian_cost)
    )

    post_mining_state = state.after_mining(blueprint)

    if can_buy_ore_robot:
        new_state = post_mining_state.post_buy_ore_robot(blueprint)
        if new_state not in state_history or turn < state_history[new_state]:
            options.append(StateAllowedToBuy(new_state, True, True, True))
            state_history[new_state] = turn
    if can_buy_clay_robot:
        new_state = post_mining_state.post_buy_clay_robot(blueprint)
        if new_state not in state_history or turn < state_history[new_state]:
            options.append(StateAllowedToBuy(new_state, True, True, True))
            state_history[new_state] = turn
    if can_buy_obsidian_robot:
        new_state = post_mining_state.post_buy_obsidian_robot(blueprint)
        if new_state not in state_history or turn < state_history[new_state]:
            options.append(StateAllowedToBuy(new_state, True, True, True))
            state_history[new_state] = turn
    if can_buy_geode_robot:
        new_state = post_mining_state.post_buy_geode_robot(blueprint)
        if new_state not in state_history or turn < state_history[new_state]:
            options.append(StateAllowedToBuy(new_state, True, True, True))
            state_history[new_state] = turn
    if (
        not (can_buy_ore_robot and can_buy_clay_robot and can_buy_obsidian_robot)
        and not can_buy_geode_robot
    ):
        if (
            post_mining_state not in state_history
            or turn < state_history[post_mining_state]
        ):
            options.append(
                StateAllowedToBuy(
                    post_mining_state,
                    not can_buy_ore_robot and state_allowed.ore_robot_valid,
                    not can_buy_clay_robot and state_allowed.clay_robot_valid,
                    not can_buy_obsidian_robot and state_allowed.obsidian_robot_valid,
                )
            )
            state_history[post_mining_state] = turn
    if len(options) == 0:
        return 0
    scores = []

    for opt in options:
        scores.append(rec_run_turn(opt, blueprint, turn + 1, state_history, end_turn))
    return max(scores)


if __name__ == "__main__":
    blueprints: "list[Blueprint]" = []

    for line in sys.argv[1].split("\n"):
        nums = re.findall(r"\d+", line)
        blueprints.append(
            Blueprint(
                int(nums[0]),
                int(nums[1]),
                int(nums[2]),
                int(nums[3]),
                int(nums[4]),
                int(nums[5]),
                int(nums[6]),
            )
        )

    scores = []

    for blueprint in blueprints:
        default_turn_state = State(0, 0, 0, 0, 1, 0, 0, 0)
        scores.append(
            rec_run_turn(
                StateAllowedToBuy(default_turn_state, True, True, True),
                blueprint,
                1,
                dict(),
                25,
            )
        )

    pprint(blueprints)
    pprint(scores)

    score_acc = 0
    for idx, score in enumerate(scores):
        score_acc += (idx + 1) * score
        print(f"Blueprint {idx + 1} has score {idx + 1 * score}")
        print(f"{score_acc = }")

    # part 2

    part2_scores = []

    for blueprint in blueprints[:3]:
        default_turn_state = State(0, 0, 0, 0, 1, 0, 0, 0)
        part2_scores.append(
            rec_run_turn(
                StateAllowedToBuy(default_turn_state, True, True, True),
                blueprint,
                1,
                dict(),
                33,
            )
        )

    print(f"{part2_scores = }")
