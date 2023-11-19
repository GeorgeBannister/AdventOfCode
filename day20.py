#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Pos:
    value: int
    index: int

    def dec_idx(self, list_len: int):
        new_index = self.index - 1
        if new_index == -1:
            new_index = list_len - 1
        self.index = new_index

    def inc_idx(self, list_len: int):
        new_index = self.index + 1
        if new_index == list_len:
            new_index = 0
        self.index = new_index


def swap_places(list_container: list[Pos], idx_1: int, idx_2: int) -> None:
    lc_index_1 = 0
    lc_index_2 = 0
    for idx, item in enumerate(list_container):
        if item.index == idx_1:
            lc_index_1 = idx
        if item.index == idx_2:
            lc_index_2 = idx
    tmp = list_container[lc_index_1].index
    list_container[lc_index_1].index = list_container[lc_index_2].index
    list_container[lc_index_2].index = tmp


# [4, 5, 6, <1>, 7, 8, 9] => [4, 5, 6, 7, <1>, 8, 9]


# [4, {-2}, 5, 6, 7, 8, 9] => [4, 5, 6, 7, 8, {-2}, 9]   len=7
#  0   {1}   2  3  4  5  6     0  1  2  3  4  {5}   6


def solve_part_1_list(input_list: list[int], num_times: int) -> list[int]:
    list_len = len(input_list)
    pos_list: list[Pos] = []

    for idx, val in enumerate(input_list):
        pos_list.append(Pos(val, idx))

    for _ in range(num_times):
        for pos_val in pos_list:
            # It takes list len - 1 moves to go full circle
            mod_movement = pos_val.value % (list_len - 1)

            if mod_movement > 0 and pos_val.index + mod_movement >= list_len:
                mod_movement = mod_movement - (list_len - 1)

            if mod_movement < 0 and pos_val.index + mod_movement < 0:
                mod_movement = list_len - 1 + mod_movement

            while mod_movement > 0:
                index_1 = pos_val.index
                index_2 = (index_1 + 1) % list_len
                swap_places(pos_list, index_1, index_2)
                mod_movement -= 1

            while mod_movement < 0:
                index_1 = pos_val.index
                index_2 = (index_1 + -1) % list_len
                swap_places(pos_list, index_1, index_2)
                mod_movement += 1

            # print(f"New index is {pos_val.index}")
            # print_list = []
            # for x in range(0, list_len):
            #    for item in pos_list:
            #        if item.index == x:
            #            print_list.append(item.value)
            # print(f"Now list looks like {print_list}")

    ret_list = []

    for x in range(0, list_len):
        for item in pos_list:
            if item.index == x:
                ret_list.append(item.value)

    print(ret_list)
    return ret_list


def get_part_1_score(target_list: list[int]) -> int:
    list_len = len(target_list)
    zero_index = target_list.index(0)
    idxs = (
        (zero_index + 1000) % list_len,
        (zero_index + 2000) % list_len,
        (zero_index + 3000) % list_len,
    )
    to_ret = 0
    for idx in idxs:
        to_ret += target_list[idx]
    print(f"{to_ret = }")
    return to_ret


def solve_part_2_list(input_list: list[int]) -> list[int]:
    decryption_key = 811589153
    decrypted_list = [x * decryption_key for x in input_list]
    return solve_part_1_list(decrypted_list, 10)


if __name__ == "__main__":
    inp = sys.argv[1]

    # PART 1

    test_sorted = solve_part_1_list([1, 2, -3, 3, -2, 0, 4], 1)

    assert test_sorted == [1, 2, -3, 4, 0, 3, -2]
    assert get_part_1_score(test_sorted) == 3

    part_1_list = [int(x) for x in inp.splitlines()]

    print(get_part_1_score(solve_part_1_list(part_1_list), 1))
    # PART 2

    test_2_sorted = solve_part_2_list([1, 2, -3, 3, -2, 0, 4])
    print(f"{test_2_sorted = }")
    assert test_2_sorted == [
        0,
        -2434767459,
        1623178306,
        3246356612,
        -1623178306,
        2434767459,
        811589153,
    ]
    part_2_list = [int(x) for x in inp.splitlines()]
    print(get_part_1_score(solve_part_2_list(part_2_list)))
