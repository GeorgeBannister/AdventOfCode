import re

inp = '''Sensor at x=3999724, y=2000469: closest beacon is at x=4281123, y=2282046
Sensor at x=3995530, y=8733: closest beacon is at x=3321979, y=-692911
Sensor at x=3016889, y=2550239: closest beacon is at x=2408038, y=2645605
Sensor at x=3443945, y=3604888: closest beacon is at x=3610223, y=3768674
Sensor at x=168575, y=491461: closest beacon is at x=1053731, y=-142061
Sensor at x=2820722, y=3865596: closest beacon is at x=3191440, y=3801895
Sensor at x=2329102, y=2456329: closest beacon is at x=2408038, y=2645605
Sensor at x=3889469, y=3781572: closest beacon is at x=3610223, y=3768674
Sensor at x=3256726, y=3882107: closest beacon is at x=3191440, y=3801895
Sensor at x=3729564, y=3214899: closest beacon is at x=3610223, y=3768674
Sensor at x=206718, y=2732608: closest beacon is at x=-152842, y=3117903
Sensor at x=2178192, y=2132103: closest beacon is at x=2175035, y=2000000
Sensor at x=1884402, y=214904: closest beacon is at x=1053731, y=-142061
Sensor at x=3060435, y=980430: closest beacon is at x=2175035, y=2000000
Sensor at x=3998355, y=3965954: closest beacon is at x=3610223, y=3768674
Sensor at x=3704399, y=3973731: closest beacon is at x=3610223, y=3768674
Sensor at x=1421672, y=3446889: closest beacon is at x=2408038, y=2645605
Sensor at x=3415633, y=3916020: closest beacon is at x=3191440, y=3801895
Sensor at x=2408019, y=2263990: closest beacon is at x=2408038, y=2645605
Sensor at x=3735247, y=2533767: closest beacon is at x=4281123, y=2282046
Sensor at x=1756494, y=1928662: closest beacon is at x=2175035, y=2000000
Sensor at x=780161, y=1907142: closest beacon is at x=2175035, y=2000000
Sensor at x=3036853, y=3294727: closest beacon is at x=3191440, y=3801895
Sensor at x=53246, y=3908582: closest beacon is at x=-152842, y=3117903
Sensor at x=2110517, y=2243287: closest beacon is at x=2175035, y=2000000
Sensor at x=3149491, y=3998374: closest beacon is at x=3191440, y=3801895'''

oldInp = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''

# '(x, y)': int
# where 0 = no beacon, 1 = sensor, 2 = beacon
items = {}
sensor_beacon_pairs = []
row_of_interest = 10
max_bound = 20 #4000000
pt2_dict = {}
possibilities = set()
final_possibilities = []
mans = []

def update(sensor: tuple[int, int], beacon: tuple[int, int]) -> None:
    global row_of_interest
    global max_bound
    sx, sy = sensor
    bx, by = beacon
    man_distance = abs(sx - bx) + abs(sy - by)
    mans.append(man_distance)
    for x in range(- man_distance, man_distance + 1):
        if abs(x) + abs(row_of_interest- sy) <= man_distance:
            test_x = sx + x
            test_y = row_of_interest
            if test_y == row_of_interest:
                if not (test_x, test_y) in items:
                    items[(test_x, test_y)] = 0

    # Left to top
    dx = - man_distance - 1
    dy = 0
    while dx <= 0:
        x2 = sx + dx
        y2 = sy + dy
        if x2 >= 0 and x2 <= max_bound and y2 >=0 and y2 <= max_bound:
            possibilities.add((x2, y2))
        dx+=1
        dy+=1
    # Right to top
    dx = man_distance + 1
    dy = 0
    while dx >= 0:
        x2 = sx + dx
        y2 = sy + dy
        if x2 >= 0 and x2 <= max_bound and y2 >=0 and y2 <= max_bound:
            possibilities.add((x2, y2))
        dx-=1
        dy+=1
    # Left to bottom
    dx = - man_distance -1
    dy = 0
    while dx <= 0:
        x2 = sx + dx
        y2 = sy + dy
        if x2 >= 0 and x2 <= max_bound and y2 >=0 and y2 <= max_bound:
            possibilities.add((x2, y2))
        dx+=1
        dy-=1
    # Right to bottom
    dx = man_distance + 1
    dy = 0
    while dx >= 0:
        x2 = sx + dx
        y2 = sy + dy
        if x2 >= 0 and x2 <= max_bound and y2 >=0 and y2 <= max_bound:
            possibilities.add((x2, y2))
        dx-=1
        dy-=1

def test(y) -> int:
    count = 0
    for key in items:
        if key[1] == y:
            if items[key] != 2:
                count += 1
    return count

culled = 0

for line in oldInp.splitlines():
    nums= [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
    sensor = (nums[0], nums[1])
    beacon = (nums[2], nums[3])

    items[sensor] = 1
    items[beacon] = 2

    sensor_beacon_pairs.append((sensor, beacon))

for sb in sensor_beacon_pairs:
    sensor, beacon = sb
    update(sensor, beacon)
print ("init done")

print(test(row_of_interest))

PRE_CULL = len(possibilities)

pos_list = list(possibilities)
pos_list.sort()

def cull(s: tuple[int,int], b: tuple[int,int]):
    global culled
    s_x, s_y = s
    b_x, b_y = b
    man_distance = abs(s_x - b_x) + abs(s_y - b_y)
    for item in pos_list:
        px, py = item
        pos_man_distance = abs(s_x - px) + abs(s_y - py)
        if pos_man_distance <= (man_distance):
            pos_list.remove(item)
            culled += 1

for sb in sensor_beacon_pairs:
    sensor, beacon = sb
    cull(sensor, beacon)

pos_list.sort()
print(f'{PRE_CULL = }')
print(f'{culled = }')
for key in pos_list:
    final_possibilities.append(key[0] * 4000000 + key[1])
print(f'{final_possibilities = }')

acc = []
sensors = []
beacons = []
for p in sensor_beacon_pairs:
    s, b = p
    sensors.append(s)
    beacons.append(b)

for y in range (0,21):
    for x in range (0,21):
        coord = (x, y)
        if coord in sensors:
            acc.append('s')
        elif coord in beacons:
            acc.append('b')
        elif coord in pos_list:
            acc.append('X')
        else:
            acc.append('.')

for x in range (0,21):
    to_print = acc[21*x : 21*(x+1) + 1]
    print(*to_print, sep=None)
    
print (f'{sensors = }')
print (f'{beacons = }')
print (f'{mans = }')