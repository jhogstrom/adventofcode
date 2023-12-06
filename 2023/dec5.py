from collections import defaultdict, deque
import logging
import threading
import time
from reader import get_data, timeit, set_logging

runtest = False
stardate = "5"

set_logging(True)
data = get_data(stardate, runtest)
data2 = data[:]

def get_maps(data):
    maps = defaultdict(list)
    for _ in data[1:]:
        if not _:
            continue
        if ":" in _:
            transform = _.split()[0]
            continue
        maps[transform].append([int(i) for i in _.split()])

    for k, v in maps.items():
        maps[k] = sorted(v, key=lambda x: x[1])
    return maps

def map_seed(v, maps):
    for m, transforms in maps.items():
        # logging.debug(f"Mapping: {m} => {transforms}")
        for t in transforms:
            if t[1] <= v <= t[1] + t[2] - 1:
                new_v = (v-t[1]) + t[0]
                # logging.debug(f"\t{v} => {new_v} :: [{t}] --> ({v}-{t[1]}) + {t[0]})")
                v = new_v
                break
    # logging.debug("===")
    return v


@timeit
def star1(data):
    logging.debug("running star 1")
    seeds = [int(_) for _ in data[0].split(":")[1].split()]
    maps = get_maps(data)

    # locations = []
    min_loc = None
    for s in seeds:
        loc = map_seed(s, maps)
        min_loc = min(min_loc, loc) if min_loc else loc
        # locations.append(loc)
    # print(locations)
    # print(min(locations))
    print(min_loc)


class MapRange(object):
    def __init__(self, start, end, transform):
        self.source_start = start
        self.source_end = end
        self.dest_start = start + transform
        self.dest_end = end + transform
        self.transform = transform

    def __repr__(self):
        padd = 0
        return f"{self.source_start:{padd}}..{self.source_end:{padd}} => {self.dest_start}..{self.dest_end} [{self.transform:{padd}}]"

    def identity(self, transform=0):
        """
        Create an identical range (based on dest) with a transform of 0
        """
        return MapRange(self.dest_start, self.dest_end, transform)


    # def make_new_ranges(self, ranges):
    #     new_ranges = []
    #     for r in ranges:
    #         created = 0
    #         logging.debug(f"Checking {r}")
    #         # Before
    #         if self.dest_end < r.source_start:
    #             # logging.debug(f"\t{self} is before {r}")
    #             continue
    #         # After
    #         if self.dest_start > r.source_end:
    #             # logging.debug(f"\t{self} is after {r}")
    #             continue
    #         # Contains
    #         if self.dest_start < r.source_start and self.dest_end > r.source_end:
    #             # logging.debug(f"\t{self} contains {r}")
    #             new_ranges.append(MapRange(r.dest_start, r.dest_end))
    #             created += 1
    #             continue
    #         # Contained
    #         if self.dest_start > r.source_start and self.dest_end < r.source_end:
    #             # logging.debug(f"\t{self} is contained by {r}")
    #             new_ranges.append(MapRange(r.dest_start, r.dest_end))
    #             created += 1
    #             continue
    #         if self.dest_start <= r.source_start <= self.dest_end:
    #             pass

    #         logging.debug(f"** Created {created} new ranges:")
    #         for nr in new_ranges[-created:]:
    #             logging.debug(f"\t{nr}")
    #     return new_ranges


    def merge_with(self, target_range):
        if self.dest_end < target_range.source_start:
            return None
        if self.dest_start > target_range.source_end:
            return None
        # if self.dest_end <= target_range.source_end:
        return MapRange(
                max([self.dest_start, target_range.source_start]) + target_range.transform,
                min([self.dest_end, target_range.source_end]) + target_range.transform,
                0)


@timeit
def star2(data):
    logging.debug("running star 2")
    seeds = [int(_) for _ in data[0].split(":")[1].split()]
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(MapRange(seeds[i], seeds[i] + seeds[i+1] - 1, 0))
    logging.debug(f"Seed ranges: {seed_ranges}")

    # Create a map of all the transforms
    transform_map = {}
    for m, transforms in get_maps(data).items():
        # logging.debug(f"Mapping: {m}")
        r = []
        for t in transforms:
            r.append(MapRange(t[1], t[1] + t[2] - 1, t[0]-t[1]))
        transform_map[m] = r

    # Iterate through the maps, applying them to the seed ranges to yield new seed ranges
    incoming = seed_ranges
    for m, transforms in transform_map.items():
        logging.debug(f"Applying {m}")
        new_ranges = []
        for incoming_range in incoming:
            for t in transforms:
                logging.debug(f"\tApplying {incoming_range} to {t}")
                res = incoming_range.merge_with(t)
                if res:
                    logging.debug(f"\t\t{res}")
                    new_ranges.append(res)

        incoming = new_ranges[:]
        logging.debug(f"New ranges: {new_ranges}")




# star1(data)

import concurrent.futures

def get_minimum(seed_range, maps):
    seed_count = seed_range.source_end - seed_range.source_start
    print(seed_range, seed_count)
    min_loc = None
    i = 0
    for s in range(seed_range.source_start, seed_range.source_end):
        i += 1
        if i % 1000000 == 0:
            print(f"Processed {i}/{seed_count} {i/seed_count:.2}% seeds")
        loc = map_seed(s, maps)
        min_loc = min(min_loc, loc) if min_loc else loc
    return min_loc

def star2_exp(data):
    logging.debug("running star 2_exp")
    seeds = [int(_) for _ in data[0].split(":")[1].split()]
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(MapRange(seeds[i], seeds[i] + seeds[i+1] - 1, 0))
    # seed_ranges = [MapRange(82, 82, 0)]
    maps = get_maps(data)
    min_values = []
    futures = []
    # with concurrent.futures.ProcessPoolExecutor(8) as executor:
    for seed_range in seed_ranges:
        # futures.append(executor.submit(get_minimum, seed_range, maps))
        # time.sleep(1)
        min_values.append(get_minimum(seed_range, maps))
    # locations.append(loc)
    # print(locations)
    print(min(min_values))
        # print(min([f.result() for f in futures]))


star2_exp(data2)
# star2(data2)
