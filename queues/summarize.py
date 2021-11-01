#!/usr/bin/env python3
import sys
import os
from threading import Thread
from queue import Queue, LifoQueue
from functools import cache
from operator import itemgetter
from collections import Counter
from rectangle import Rectangle

# Keep a count of each area a rectangle might have
rect_areas = Counter()
rect_queue = LifoQueue()
area_queue = Queue()


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
            rect_queue.put(rect)
        elif cmd == "MOVE":
            # Add moved version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_queue.get()
            new_rect = rect.move(vertical, horizontal)
            rect_queue.put(rect)
            rect_queue.put(new_rect)
        elif cmd == "RESIZE":
            # Add resized version of the previously read rectangle
            vertical, horizontal = [float(n) for n in data.split()]
            rect = rect_queue.get()
            new_rect = rect.resize(vertical, horizontal)
            rect_queue.put(rect)
            rect_queue.put(new_rect)


def rect_to_area():
    while not rect_queue.empty():
        rect = rect_queue.get()
        area = rect.area()
        area_queue.put(area)
        rect_queue.task_done()


def area_to_counter():
    while not area_queue.empty():
        rect_areas[area_queue.get(timeout=1)] += 1


if __name__ == '__main__':
    read_rectangles()
    for _ in range(os.cpu_count()):
        Thread(target=rect_to_area, daemon=True).start()
    rect_queue.join()
    area_to_counter()

    print("Number of rectangles computed:", sum(rect_areas.values()))
    print("Most common rectangle areas:")
    most_common = sorted(rect_areas.most_common(),
                         key=itemgetter(1), reverse=True)
    for area, count in most_common:
        print("  Area %s\t%d rectangles" % (area, count))
