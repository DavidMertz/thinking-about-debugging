#!/usr/bin/env python3
import sys
import os
from time import sleep
from collections import Counter, deque
from operator import itemgetter
from functools import cache
from threading import Thread
from rectangle import Rectangle

# Keep a count of each area a rectangle might have
rect_areas = Counter()
# A deque is a thread-safe data structure
rect_deq = deque()
area_deq = deque()


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
            rect_deq.append(rect)
        elif cmd == "MOVE":
            # Add moved version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_deq[-1]
            new_rect = rect.move(vertical, horizontal)
            rect_deq.append(new_rect)
        elif cmd == "RESIZE":
            # Add resized version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_deq[-1]
            new_rect = rect.resize(vertical, horizontal)
            rect_deq.append(new_rect)


def rect_to_area():
    while rect_deq:
        rect = rect_deq.pop()
        area = rect.area()
        area_deq.append(area)


def area_to_counter():
    while area_deq:
        rect_areas[area_deq.pop()] += 1


if __name__ == '__main__':
    read_rectangles()
    for _ in range(os.cpu_count()):
        Thread(target=rect_to_area).start()

    # Wait for the threads to empty rect_deq
    while rect_deq:
        sleep(0.01)
    area_to_counter()

    print("Number of rectangles computed:", sum(rect_areas.values()))
    print("Most common rectangle areas:")
    most_common = sorted(rect_areas.most_common(),
                         key=itemgetter(1), reverse=True)
    for area, count in most_common:
        print("  Area %s\t%d rectangles" % (area, count))
