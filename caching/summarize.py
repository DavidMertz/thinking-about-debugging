#!/usr/bin/env python3
import sys
from collections import Counter
from functools import cache
from operator import itemgetter
from rectangle import Rectangle

# Keep a count of each area a rectangle might have
rect_areas = Counter()
rect_list = list()
area_list = list()


@cache
def create_rectangle(bottom, left, top, right):
    "Creating a rectangle is expensive, reuse an existing one if available"
    return Rectangle(bottom, left, top, right)


def read_rectangles():
    for line in sys.stdin:
        cmd, data = line.split(maxsplit=1)
        if cmd == "CREATE":
            bottom, left, top, right = [float(n) for n in data.split()]
            rect = create_rectangle(bottom, left, top, right)
            rect_list.append(rect)
        elif cmd == "MOVE":
            # Add moved version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_list[-1]
            new_rect = rect.move(vertical, horizontal)
            rect_list.append(new_rect)
        elif cmd == "RESIZE":
            # Add resized version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_list[-1]
            new_rect = rect.resize(vertical, horizontal)
            rect_list.append(new_rect)


def rect_to_area():
    while rect_list:
        rect = rect_list.pop()
        area = rect.area()
        area_list.append(area)


def area_to_counter():
    while area_list:
        rect_areas[area_list.pop()] += 1


if __name__ == '__main__':
    read_rectangles()
    rect_to_area()
    area_to_counter()

    print("Number of rectangles computed:", sum(rect_areas.values()))
    print("Most common rectangle areas:")
    most_common = sorted(rect_areas.most_common(),
                         key=itemgetter(1), reverse=True)
    for area, count in most_common:
        print("  Area %s\t%d rectangles" % (area, count))
