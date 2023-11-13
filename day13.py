#! /usr/bin/env python3

import copy
import sys
import pprint

# -1 = in order | 0 = continue | 1 = fail


def list_cmp(left_list: list, right_list: list) -> int:
    while True:
        if len(left_list) == 0 and len(right_list) == 0:
            return 0
        if len(left_list) == 0:
            return -1
        if len(right_list) == 0:
            return 1
        l = left_list.pop(0)
        r = right_list.pop(0)

        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return -1
            if l > r:
                return 1

        if isinstance(l, int) and isinstance(r, list):
            x = list_cmp([l], r)
            if x == -1:
                return -1
            if x == 1:
                return 1

        if isinstance(l, list) and isinstance(r, int):
            x = list_cmp(l, [r])
            if x == -1:
                return -1
            if x == 1:
                return 1

        if isinstance(l, list) and isinstance(r, list):
            x = list_cmp(l, r)
            if x == -1:
                return -1
            if x == 1:
                return 1


def pair_is_valid(pair) -> bool:
    left_list, right_list = pair

    print(f"\n {left_list = }\n{right_list = }")

    while True:
        if len(left_list) == 0:
            return True
        if len(right_list) == 0:
            return False
        l = left_list.pop(0)
        r = right_list.pop(0)

        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            if l > r:
                return True

        if isinstance(l, int) and isinstance(r, list):
            x = list_cmp([l], r)
            if x == -1:
                return True
            if x == 1:
                return False

        if isinstance(l, list) and isinstance(r, int):
            x = list_cmp(l, [r])
            if x == -1:
                return True
            if x == 1:
                return False

        if isinstance(l, list) and isinstance(r, list):
            x = list_cmp(l, r)
            if x == -1:
                return True
            if x == 1:
                return False


if __name__ == "__main__":
    packet_pairs = []
    p2pairs = []
    pairs = sys.argv[1].split("\n\n")

    for p in pairs:
        spl = p.split("\n")
        packet_pairs.append((eval(spl[0]), eval(spl[1])))
        p2pairs.append(eval(spl[0]))
        p2pairs.append(eval(spl[1]))

    count = 0
    for idx, pair in enumerate(packet_pairs):
        if pair_is_valid(pair):
            count += idx + 1

    # part 2

    smaller_than_two = 1
    smaller_than_six = 2

    print(f"{p2pairs = }")

    for pair in p2pairs:
        if pair_is_valid((copy.deepcopy(pair), [[2]])):
            print(f"{pair} < 2")
            smaller_than_two += 1

    print(f"{p2pairs = }")

    for pair in p2pairs:
        if pair_is_valid((copy.deepcopy(pair), [[6]])):
            print(f"{pair} < 6")
            smaller_than_six += 1

    print(f"{count = }")
    print(f"{len(p2pairs) =}")
    print(
        f"{smaller_than_two = } {smaller_than_six = } a = {smaller_than_two * smaller_than_six}"
    )
