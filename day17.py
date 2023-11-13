#!/usr/bin/env python3

from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # def __eq__(self, other):
    #    return self.x == other.x and self.y == other.y

    # def __hash__(self):
    #    return hash((self.x, self.y))


@dataclass
class Rock:
    # x, y offsets from bottom left of where the rock exists
    offsets: "list[Point]"


@dataclass
class RockInstance:
    prototype: Rock
    # bottom left coord
    origin: Point


@dataclass
class State:
    collision_grid: "set[Point]"
    curr_max_height: int
    jet_pattern: str
    jet_pattern_iterator: int
    jet_pattern_len: int
    rock_iterator: int
    rock_count: int
    current_rock: RockInstance | None


rocks: "list[Rock]" = [
    Rock([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]),
    Rock(
        [
            Point(1, 0),
            Point(0, 1),
            Point(1, 1),
            Point(2, 1),
            Point(1, 2),
        ]
    ),
    Rock(
        [
            Point(0, 0),
            Point(1, 0),
            Point(2, 0),
            Point(2, 1),
            Point(2, 2),
        ]
    ),
    Rock([Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)]),
    Rock([Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]),
]

# ( (7 wide bool), rock index, wind index) => (turn, current height)
memo: "dict" = dict()


def position_is_valid(state: State, instance: RockInstance) -> bool:
    for offset in instance.prototype.offsets:
        coord = offset + instance.origin
        if (
            coord in state.collision_grid
            or coord.x == -1
            or coord.x == 7
            or coord.y == -1
        ):
            return False
    return True


def update_max_height(state: State):
    global curr_max_height
    for point in state.collision_grid:
        if point.y > curr_max_height:
            curr_max_height = point.y


def wind(state: State) -> RockInstance:
    direction = state.jet_pattern[state.jet_pattern_iterator]
    state.jet_pattern_iterator += 1
    state.jet_pattern_iterator %= state.jet_pattern_len
    if direction == "<":
        return RockInstance(
            state.current_rock.prototype, state.current_rock.origin + Point(-1, 0)
        )
    elif direction == ">":
        return RockInstance(
            state.current_rock.prototype, state.current_rock.origin + Point(1, 0)
        )
    print("ERROR BAD WIND")
    exit(1)


def gravity(state: State) -> RockInstance:
    return RockInstance(
        state.current_rock.prototype, state.current_rock.origin + Point(0, -1)
    )


def spawn_rock(state: State):
    state.current_rock = RockInstance(
        rocks[state.rock_iterator], Point(2, state.curr_max_height + 4)
    )
    state.rock_iterator += 1
    state.rock_iterator %= 5


def crystalise_rock(state: State):
    for offset in state.current_rock.prototype.offsets:
        coord = offset + state.current_rock.origin
        state.collision_grid.add(coord)
        if coord.y > state.curr_max_height:
            state.curr_max_height = coord.y
    state.rock_count += 1


global height_skip_delta
have_jumped = False

# ( (7 wide bool), rock index, wind index) => (turn, current height)


def fill_memo(state: State):
    global height_skip_delta
    global have_jumped
    bool_tup = tuple(
        Point(x, state.curr_max_height - y) in state.collision_grid
        for x in range(0, 7)
        for y in range(0, 20)
    )
    key = (bool_tup, state.rock_iterator, state.jet_pattern_iterator)
    value = (state.rock_count, state.curr_max_height)
    if key in memo and not have_jumped:
        have_jumped = True
        print(f"{memo[key] = } => {value = }")
        jump_turns = value[0] - memo[key][0]
        height_per_jump = value[1] - memo[key][1]

        print(f"it takes {jump_turns} turns to get {height_per_jump} height")
        number_of_jumps_needed = (1000000000000 - state.rock_count) // jump_turns
        state.rock_count += number_of_jumps_needed * jump_turns
        height_skip_delta = number_of_jumps_needed * height_per_jump
        print(f"{height_skip_delta = }")

    memo[key] = value


def play_for_x_rocks(state: State, num_rocks: int):
    global height_skip_delta
    while state.rock_count < num_rocks:
        # print(f"{state.rock_count = }")
        spawn_rock(state)
        rock_has_settled = False
        while not rock_has_settled:
            wind_shadow = wind(state)
            if position_is_valid(state, wind_shadow):
                state.current_rock = wind_shadow
            gravity_shadow = gravity(state)
            if position_is_valid(state, gravity_shadow):
                state.current_rock = gravity_shadow
            else:
                crystalise_rock(state)
                fill_memo(state)
                rock_has_settled = True
    print(f"{state.curr_max_height = }")
    print(f"ans = {state.curr_max_height + height_skip_delta + 1}")


def print_window(state: State, top_left: tuple, bottom_right: tuple):
    for y in range(top_left[1], bottom_right[1], -1):
        row_buffer = ""
        for x in range(top_left[0], bottom_right[0]):
            if (x, y) == (-1, -1) or (x, y) == (7, -1):
                row_buffer += "+"
            elif y == -1:
                row_buffer += "-"
            elif x == -1 or x == 7:
                row_buffer += "|"
            elif Point(x, y) in state.collision_grid:
                row_buffer += "#"
            else:
                row_buffer += "."
        print(row_buffer)


if __name__ == "__main__":
    jet_pattern = sys.argv[1]
    game_state = State(set(), -1, jet_pattern, 0, len(jet_pattern), 0, 0, None)
    play_for_x_rocks(game_state, 1000000000000)
    # print()
    # print_window(game_state, (-1, 20), (8, -2))
