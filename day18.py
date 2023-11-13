#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    def is_touching(self, other) -> bool:
        if (
            (abs(self.x - other.x) == 1 and self.y == other.y and self.z == other.z)
            or (self.x == other.x and abs(self.y - other.y) == 1 and self.z == other.z)
            or (self.x == other.x and self.y == other.y and abs(self.z - other.z) == 1)
        ):
            return True
        return False

    def get_adjacent(self):
        adjacent_list = []
        adjacent_list.append(Point3D(self.x - 1, self.y, self.z))
        adjacent_list.append(Point3D(self.x + 1, self.y, self.z))
        adjacent_list.append(Point3D(self.x, self.y - 1, self.z))
        adjacent_list.append(Point3D(self.x, self.y + 1, self.z))
        adjacent_list.append(Point3D(self.x, self.y, self.z - 1))
        adjacent_list.append(Point3D(self.x, self.y, self.z + 1))
        return adjacent_list

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))


part_2_sa = 0


def explore(
    point: Point3D,
    target_point: Point3D,
    orig_point: Point3D,
    explored_set: set,
    solid_set: set,
):
    global part_2_sa
    for x_delta, y_delta, z_delta in [
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, -1),
        (0, -1, 0),
        (-1, 0, 0),
    ]:
        delta_point = Point3D(x_delta, y_delta, z_delta)
        new_point = point + delta_point
        if (
            new_point in solid_set
            or new_point in explored_set
            or new_point.x > target_point.x
            or new_point.y > target_point.y
            or new_point.z > target_point.z
            or new_point.x < orig_point.x
            or new_point.y < orig_point.y
            or new_point.z < orig_point.z
        ):
            continue
        explored_set.add(new_point)
        for solid_point in solid_set:
            if new_point.is_touching(solid_point):
                part_2_sa += 1
        explore(new_point, target_point, orig_point, explored_set, solid_set)


if __name__ == "__main__":
    sys.setrecursionlimit(10000000)
    points: "list[Point3D]" = []
    surface_area: int = 0

    for line in sys.argv[1].splitlines():
        nums: "list[int]" = [int(x) for x in re.findall(r"\d+", line)]
        points.append(Point3D(nums[0], nums[1], nums[2]))

    for point in points:
        surface_area += 6

    for point in points:
        for second_point in points:
            if not point == second_point:
                if point.is_touching(second_point):
                    surface_area -= 1

    print(f"{surface_area = }")

    ###### PART 2 ######

    points_set: set[Point3D] = set(points)
    explored_set: set[Point3D] = set()

    # Draw a "Box" around the shape (+ 1 each side)
    # Do a search to try to reach every spot in the box

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0

    for point in points:
        if point.x < min_x:
            min_x = point.x
        if point.x > max_x:
            max_x = point.x
        if point.y < min_y:
            min_y = point.y
        if point.y > max_y:
            max_y = point.y
        if point.z < min_z:
            min_z = point.z
        if point.z > max_z:
            max_z = point.z

    max_x += 1
    max_y += 1
    max_z += 1
    min_x -= 1
    min_y -= 1
    min_z -= 1

    start = Point3D(min_x, min_y, min_z)
    end = Point3D(max_x, max_y, max_z)

    explore(start, end, start, explored_set, points_set)
    print(f"{part_2_sa = }")
    ######################
