# Source: https://github.com/enihsyou/The-Farmer-Was-Replaced
# Source commit: 37a97b58e15dc60bb6aff8829eeb58293be18b39
# MIT License
# 
# Copyright (c) 2026 enihsyou
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Adaptation: bounded trial; no empty fertilizer calls; explicit join.
# Geometric cycle tables; no seed-specific values.
CYCLE_STEPS = {
    (3, True): [North, North, North, North, North, West, West, South, East, South, West, South, East, South, West, South, East, East],
    (3, False): [North, North, North, North, North, East, East, South, West, South, East, South, West, South, East, South, West, West],
    (4, True): [North, North, North, North, North, North, North, West, West, West, South, East, East, South, West, West, South, East, East, South, West, West, South, East, East, South, West, West, South, East, East, East],
    (4, False): [North, North, North, North, North, North, North, East, East, East, South, West, West, South, East, East, South, West, West, South, East, East, South, West, West, South, East, East, South, West, West, West],
}
CYCLE_INDEX = {
    (3, True): {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (-1, 5): 6, (-2, 5): 7, (-2, 4): 8, (-1, 4): 9, (-1, 3): 10, (-2, 3): 11, (-2, 2): 12, (-1, 2): 13, (-1, 1): 14, (-2, 1): 15, (-2, 0): 16, (-1, 0): 17},
    (3, False): {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (1, 5): 6, (2, 5): 7, (2, 4): 8, (1, 4): 9, (1, 3): 10, (2, 3): 11, (2, 2): 12, (1, 2): 13, (1, 1): 14, (2, 1): 15, (2, 0): 16, (1, 0): 17},
    (4, True): {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (0, 6): 6, (0, 7): 7, (-1, 7): 8, (-2, 7): 9, (-3, 7): 10, (-3, 6): 11, (-2, 6): 12, (-1, 6): 13, (-1, 5): 14, (-2, 5): 15, (-3, 5): 16, (-3, 4): 17, (-2, 4): 18, (-1, 4): 19, (-1, 3): 20, (-2, 3): 21, (-3, 3): 22, (-3, 2): 23, (-2, 2): 24, (-1, 2): 25, (-1, 1): 26, (-2, 1): 27, (-3, 1): 28, (-3, 0): 29, (-2, 0): 30, (-1, 0): 31},
    (4, False): {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (0, 6): 6, (0, 7): 7, (1, 7): 8, (2, 7): 9, (3, 7): 10, (3, 6): 11, (2, 6): 12, (1, 6): 13, (1, 5): 14, (2, 5): 15, (3, 5): 16, (3, 4): 17, (2, 4): 18, (1, 4): 19, (1, 3): 20, (2, 3): 21, (3, 3): 22, (3, 2): 23, (2, 2): 24, (1, 2): 25, (1, 1): 26, (2, 1): 27, (3, 1): 28, (3, 0): 29, (2, 0): 30, (1, 0): 31},
}


# Generated geometric cycles; duplicated spur is movement-only.
SEVEN_LEFT_NODES = [(-3, -3), (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-3, 3), (-2, 3), (-1, 3), (-1, 2), (-2, 2), (-2, 1), (-1, 1), (-1, 0), (-2, 0), (-2, -1), (-1, -1), (0, -1), (0, -2), (0, -3), (-1, -3), (-1, -2), (-2, -2), (-2, -3)]
SEVEN_LEFT_FLAGS = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
SEVEN_LEFT_INDEX = {(-3, -3): 0, (-3, -2): 1, (-3, -1): 2, (-3, 0): 3, (-3, 1): 4, (-3, 2): 5, (-3, 3): 6, (-2, 3): 7, (-1, 3): 8, (-1, 2): 9, (-2, 2): 10, (-2, 1): 11, (-1, 1): 12, (-1, 0): 13, (-2, 0): 14, (-2, -1): 15, (-1, -1): 16, (0, -1): 17, (0, -2): 18, (0, -3): 19, (-1, -3): 20, (-1, -2): 21, (-2, -2): 22, (-2, -3): 23}
SEVEN_LEFT_STEPS = [North, North, North, North, North, North, East, East, South, West, South, East, South, West, South, East, East, South, South, West, North, West, South, West]
SEVEN_RIGHT_NODES = [(0, 1), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1), (3, -2), (3, -3), (2, -3), (1, -3), (1, -2), (2, -2), (2, -1), (1, -1), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (1, 1)]
SEVEN_RIGHT_FLAGS = [True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
SEVEN_RIGHT_INDEX = {(0, 1): 0, (0, 0): 1, (0, 2): 3, (0, 3): 4, (1, 3): 5, (2, 3): 6, (3, 3): 7, (3, 2): 8, (3, 1): 9, (3, 0): 10, (3, -1): 11, (3, -2): 12, (3, -3): 13, (2, -3): 14, (1, -3): 15, (1, -2): 16, (2, -2): 17, (2, -1): 18, (1, -1): 19, (1, 0): 20, (2, 0): 21, (2, 1): 22, (2, 2): 23, (1, 2): 24, (1, 1): 25}
SEVEN_RIGHT_STEPS = [South, North, North, North, East, East, East, South, South, South, South, South, South, West, West, North, East, North, West, North, East, North, North, West, South, West]

s = get_world_size()
m = s - 1
W = 0.8
B = 3.0


def traverse_rectangle(fn, w, h, mirror):
    if mirror:
        base, back = (West, East)
    else:
        base, back = (East, West)
    fn()
    for i in range(1, h):
        move(North)
        fn()
    move(base)
    for i in range(h, 0, -2):
        for j in range(w, 1, -1):
            fn()
            if j != 2:
                move(base)
        move(South)
        for j in range(w, 1, -1):
            fn()
            if j != 2:
                move(back)
        if i != 2:
            move(South)
    move(back)


def traverse_spiral(fn, w, h, cww):
    if cww:
        pair_even = (East, South)
        pair_odd = (West, North)
    else:
        pair_even = (West, North)
        pair_odd = (East, South)
    fn()
    i = 0
    while True:
        if not (w and h):
            break
        if i % 2:
            dir_x, dir_y = pair_even
        else:
            dir_x, dir_y = pair_odd
        for _ in range(w):
            move(dir_x)
            fn()
        for _ in range(h):
            move(dir_y)
            fn()
        w -= 1
        h -= 1
        i += 1


def seven_loop_part_cw(fn):
    for _ in range(2):
        move(North)
        fn()
    move(North)
    traverse_spiral(fn, 3, 6, False)
    for _ in range(2):
        move(West)
        move(North)


def seven_loop_part_cww(fn):
    for _ in range(2):
        move(South)
        fn()
    move(South)
    traverse_spiral(fn, 3, 6, True)
    for _ in range(2):
        move(East)
        move(South)


def work_drone_task(size):
    start = (get_pos_x(), get_pos_y())
    target_water = {6: 0.8, 7: 0.7, 8: 0.6}[size]

    # use two stacks to simulate a queue, because pop() is faster than pop(0)
    unripes_in_stack = []
    unripes_out_stack = []

    def dequeue():
        if not unripes_out_stack:
            while unripes_in_stack:
                unripes_out_stack.append(unripes_in_stack.pop())
        return unripes_out_stack.pop()

    def plant_pumpkin_no_till():
        plant(Entities.Pumpkin)

    def plant_pumpkin_with_till():
        till()
        plant_pumpkin_no_till()

    plant_pumpkin = plant_pumpkin_with_till

    def check_pumpkin():
        if can_harvest():
            return
        just_planted = plant(Entities.Pumpkin)
        if just_planted and get_time() - start_time > B + 0.6 * (size - 7) and len(unripes_in_stack) + len(unripes_out_stack) <= 1 and num_items(Items.Fertilizer) > 0:
            if use_item(Items.Fertilizer):
                # Fertilizer can immediately kill the crop. Restart growth now
                # instead of leaving a dead tile for the next queue visit.
                if get_entity_type() == Entities.Dead_Pumpkin:
                    plant(Entities.Pumpkin)
        if can_harvest():
            return
        if get_water() < target_water and num_items(Items.Water) > 0:
            use_item(Items.Water)
        if can_harvest():
            return
        unripes_in_stack.append((get_pos_x(), get_pos_y()))

    def cycle_pumpkin():
        while (unripes_in_stack or unripes_out_stack) and get_time() < 1600 and num_items(Items.Pumpkin) < 200000000:
            last_d = move_to_without_last_move(dequeue())
            if last_d:
                # 移动之前就能判断是否成熟
                group_id = measure()
                if group_id != None and group_id == measure(last_d):
                    continue
                move(last_d)
            check_pumpkin()

    def traverse_rotating(fn, width, height, mirror):
        origin_x = start[0]
        if not mirror:
            origin_x += 1
            # Spawn beside the parent's last repair, then enter the nearest right cell.
            while get_pos_x() < origin_x:
                move(East)
        local = (get_pos_x() - origin_x, get_pos_y() - start[1])
        key = (width, mirror)
        first = CYCLE_INDEX[key][local]
        steps = CYCLE_STEPS[key]
        for chunk in range(first, len(steps), 4):
            if num_items(Items.Pumpkin) >= 200000000:
                return
            for i in range(chunk, min(chunk + 4, len(steps))):
                fn()
                move(steps[i])
        for chunk in range(0, first, 4):
            if num_items(Items.Pumpkin) >= 200000000:
                return
            for i in range(chunk, min(chunk + 4, first)):
                fn()
                move(steps[i])

    def one_side_n(size, mirror):
        size_2 = size * 2

        def fn():
            traverse_rotating(plant_pumpkin, size, size_2, mirror)
            traverse_rotating(check_pumpkin, size, size_2, mirror)
            cycle_pumpkin()

        return fn

    def wait_merge(right_drone):
        wait_for(right_drone)
        if num_items(Items.Pumpkin) < 200000000:
            harvest()

    def while_round_6():
        left_side = one_side_n(3, True)
        right_side = one_side_n(3, False)
        right_drone = spawn_drone(right_side)
        left_side()
        wait_merge(right_drone)

    def while_round_8():
        left_side = one_side_n(4, True)
        right_side = one_side_n(4, False)
        right_drone = spawn_drone(right_side)
        left_side()
        wait_merge(right_drone)

    def traverse_seven(fn, mirror):
        if mirror:
            nodes = SEVEN_LEFT_NODES
            flags = SEVEN_LEFT_FLAGS
            indexes = SEVEN_LEFT_INDEX
            steps = SEVEN_LEFT_STEPS
        else:
            nodes = SEVEN_RIGHT_NODES
            flags = SEVEN_RIGHT_FLAGS
            indexes = SEVEN_RIGHT_INDEX
            steps = SEVEN_RIGHT_STEPS
        local = (get_pos_x() - start[0], get_pos_y() - start[1])
        if local not in indexes:
            best = 100
            entry = nodes[0]
            for pos in indexes:
                distance = abs(pos[0] - local[0]) + abs(pos[1] - local[1])
                if distance < best:
                    best = distance
                    entry = pos
            move_to((start[0] + entry[0], start[1] + entry[1]))
            local = entry
        first = indexes[local]
        for chunk in range(first, len(steps), 4):
            if num_items(Items.Pumpkin) >= 200000000:
                return
            for i in range(chunk, min(chunk + 4, len(steps))):
                if flags[i]:
                    fn()
                move(steps[i])
        for chunk in range(0, first, 4):
            if num_items(Items.Pumpkin) >= 200000000:
                return
            for i in range(chunk, min(chunk + 4, first)):
                if flags[i]:
                    fn()
                move(steps[i])

    def right_seven():
        traverse_seven(plant_pumpkin, False)
        traverse_seven(check_pumpkin, False)
        cycle_pumpkin()

    def while_round_7():
        helper = spawn_drone(right_seven)
        traverse_seven(plant_pumpkin, True)
        traverse_seven(check_pumpkin, True)
        cycle_pumpkin()
        wait_merge(helper)

    if size == 6:
        while_round = while_round_6
    if size == 7:
        while_round = while_round_7
    if size == 8:
        while_round = while_round_8
    while num_items(Items.Pumpkin) < 200000000 and get_time() < 1600:
        start_time = get_time()
        target_water = {6: 0.8, 7: 0.7, 8: 0.6}[size]
        if start_time < 90:
            target_water = 0.4
        while_round()
        unripes_in_stack = []
        unripes_out_stack = []
        plant_pumpkin = plant_pumpkin_no_till


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx_east = (tx - cx) % s
    dx_west = s - dx_east
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)

    dy_north = (ty - cy) % s
    dy_south = s - dy_north
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def move_to_without_last_move(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx = abs(tx - cx)
    dy = abs(ty - cy)
    if dx == 0 and dy == 0:
        return None
    if cx < tx:
        dir_x = East
    else:
        dir_x = West
    if cy < ty:
        dir_y = North
    else:
        dir_y = South

    if dy > 0:
        dy -= 1
        return_d = dir_y
    elif dx > 0:
        dx -= 1
        return_d = dir_x
    for _ in range(dx):
        move(dir_x)
    for _ in range(dy):
        move(dir_y)
    return return_d


def straight_move_do(side_length, d, do):
    def fn():
        for _ in range(side_length):
            move(d)
        do()

    return fn


drones = {
    (3, 3): 7,
    (11, 0): 8,
    (20, 0): 8,
    (28, 0): 6,
    (3, 8): 8,
    (12, 12): 7,
    (19, 19): 7,
    (19, 9): 6,
    (11, 17): 6,
    (27, 16): 8,
    (28, 11): 7,
    (3, 17): 8,
    (2, 26): 6,
    (11, 24): 8,
    (20, 24): 8,
    (28, 26): 6,
}

# Main drone owns the final patch, leaving exactly 32 worker slots.
def launch_patch(pos, size):
    move_to(pos)
    work_drone_task(size)

positions = list(drones)
for i in range(len(positions) - 1):
    pos = positions[i]
    spawn_drone(launch_patch, pos, drones[pos])
pos = positions[len(positions) - 1]
launch_patch(pos, drones[pos])

while num_drones() > 1:
    change_hat(Hats.Straw_Hat)
quick_print("PUMPKIN REFERENCE MULTI", get_time(), num_items(Items.Pumpkin))