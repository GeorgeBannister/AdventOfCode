#!/usr/bin/env python3

import sys
from pprint import pprint
from dataclasses import dataclass

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II


@dataclass(frozen=True)
class Valve:
    flow_rate: int
    leads_to: list


@dataclass(frozen=True)
class State:
    turn: int
    at_valve: str
    cumulative_flow: int
    valves_on: frozenset


@dataclass(frozen=True)
class StateEle:
    turn: int
    at_valves: frozenset
    cumulative_flow: int
    valves_on: frozenset


@dataclass(frozen=True)
class OldStates:
    at_valves: frozenset
    valves_on: frozenset


valves: "dict[Valve]" = dict()
useful_valves = set()
prev_states = set()

prev_state_with_score = dict()


def update_flow(state: State) -> State:
    cum_flow = state.cumulative_flow
    for valve in state.valves_on:
        cum_flow += valves[valve].flow_rate
    return State(state.turn, state.at_valve, cum_flow, state.valves_on)


def update_flow_elephant(state: StateEle) -> StateEle:
    cum_flow = state.cumulative_flow
    for valve in state.valves_on:
        cum_flow += valves[valve].flow_rate
    return StateEle(
        state.turn,
        state.at_valves,
        cum_flow,
        state.valves_on,
    )


def take_turn(states: "set[State]") -> int:
    if next(iter(states)).turn == 31:
        max = 0
        for state in states:
            if state.cumulative_flow > max:
                max = state.cumulative_flow
        return max
    else:
        print(next(iter(states)).turn)

    new_states = set()

    max_cum_flow = 0
    for state in states:
        max_cum_flow = (
            state.cumulative_flow
            if state.cumulative_flow > max_cum_flow
            else max_cum_flow
        )

    for state in states:
        updated_state = update_flow(state)

        if state in prev_states:
            continue
        prev_states.add(state)

        if state.turn > 14 and state.cumulative_flow < (max_cum_flow / 1.5):
            continue

        if state.turn > 22 and state.cumulative_flow < (max_cum_flow / 1.3):
            continue

        if state.turn > 25 and state.cumulative_flow < (max_cum_flow / 1.2):
            continue

        if state.at_valve not in state.valves_on:
            new_states.add(
                State(
                    updated_state.turn + 1,
                    updated_state.at_valve,
                    updated_state.cumulative_flow,
                    frozenset([*updated_state.valves_on, updated_state.at_valve]),
                )
            )
        for possible_location in valves[updated_state.at_valve].leads_to:
            new_states.add(
                State(
                    updated_state.turn + 1,
                    possible_location,
                    updated_state.cumulative_flow,
                    updated_state.valves_on,
                )
            )

    return take_turn(new_states)


def take_turn_ele(states: "set[StateEle]") -> int:
    if next(iter(states)).turn == 27:
        max = 0
        for state in states:
            if state.cumulative_flow > max:
                max = state.cumulative_flow
        return max
    else:
        print(next(iter(states)).turn)

    new_states = set()

    max_cum_flow = 0
    for state in states:
        max_cum_flow = (
            state.cumulative_flow
            if state.cumulative_flow > max_cum_flow
            else max_cum_flow
        )

    set_contains_all_valves = False
    all_valves_best_score = 0

    for state in states:
        updated_state = update_flow_elephant(state)

        curr_state = OldStates(updated_state.at_valves, updated_state.valves_on)

        if curr_state in prev_state_with_score:
            if updated_state.cumulative_flow < prev_state_with_score[curr_state]:
                continue
        prev_state_with_score[curr_state] = updated_state.cumulative_flow

        if len(updated_state.valves_on) == len(useful_valves):
            new_states.add(
                StateEle(
                    updated_state.turn + 1,
                    updated_state.at_valves,
                    updated_state.cumulative_flow,
                    updated_state.valves_on,
                )
            )
            set_contains_all_valves = True

            if updated_state.cumulative_flow > all_valves_best_score:
                all_valves_best_score = updated_state.cumulative_flow
            continue

        if state.turn > 6 and state.cumulative_flow < (max_cum_flow / 2):
            continue

        if state.turn > 8 and state.cumulative_flow < (max_cum_flow / 1.6):
            continue

        if state.turn > 10 and state.cumulative_flow < (max_cum_flow / 1.4):
            continue

        if state.turn > 12 and state.cumulative_flow < (max_cum_flow / 1.3):
            continue

        if state.turn > 14 and state.cumulative_flow < (max_cum_flow / 1.2):
            continue

        positions = sorted(updated_state.at_valves)

        if len(positions) == 1:
            positions.append(positions[0])

        me_cursor, ele_cursor = positions

        i_can_turn_valve = (
            me_cursor not in updated_state.valves_on and me_cursor in useful_valves
        )
        ele_can_turn_valve = (
            ele_cursor not in updated_state.valves_on and ele_cursor in useful_valves
        )

        if i_can_turn_valve and ele_can_turn_valve:
            new_states.add(
                StateEle(
                    updated_state.turn + 1,
                    frozenset([me_cursor, ele_cursor]),
                    updated_state.cumulative_flow,
                    frozenset([*updated_state.valves_on, me_cursor, ele_cursor]),
                )
            )

        if i_can_turn_valve:
            for possible_ele_location in valves[ele_cursor].leads_to:
                new_states.add(
                    StateEle(
                        updated_state.turn + 1,
                        frozenset([me_cursor, possible_ele_location]),
                        updated_state.cumulative_flow,
                        frozenset([*updated_state.valves_on, me_cursor]),
                    )
                )

        if ele_can_turn_valve:
            for possible_me_location in valves[me_cursor].leads_to:
                new_states.add(
                    StateEle(
                        updated_state.turn + 1,
                        frozenset([possible_me_location, ele_cursor]),
                        updated_state.cumulative_flow,
                        frozenset([*updated_state.valves_on, ele_cursor]),
                    )
                )

        for possible_me_location in valves[me_cursor].leads_to:
            for possible_ele_location in valves[ele_cursor].leads_to:
                new_states.add(
                    StateEle(
                        updated_state.turn + 1,
                        frozenset([possible_me_location, possible_ele_location]),
                        updated_state.cumulative_flow,
                        updated_state.valves_on,
                    )
                )

    if set_contains_all_valves:
        filtered_set = {
            x for x in new_states if x.cumulative_flow >= all_valves_best_score
        }
        return take_turn_ele(filtered_set)

    filtered_set = new_states

    return take_turn_ele(filtered_set)


if __name__ == "__main__":
    arg = (
        sys.argv[1]
        .replace(",", "")
        .replace("s", "")
        .replace("Valve ", "")
        .replace("ha flow rate=", "")
        .replace("; tunnel", "")
        .replace("lead", "")
        .replace("to", "")
        .replace("valve", "")
    )
    args = arg.split("\n")

    for line in args:
        line_split = line.split()
        valves[line_split[0]] = Valve(int(line_split[1]), line_split[2:])
        if int(line_split[1]) > 0:
            useful_valves.add(line_split[0])

    initial_state = State(1, "AA", 0, frozenset())
    initial_state_ele = StateEle(1, frozenset(["AA"]), 0, frozenset())

    pprint(valves)

    pprint(initial_state)

    # best_score = take_turn({initial_state})
    # print(f"{best_score = }")

    best_ele_score = take_turn_ele({initial_state_ele})
    print(f"{best_ele_score = }")
