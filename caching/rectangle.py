from functools import cache
from random import random
from time import sleep


class Rectangle():
    "Define a rectangle object on Cartesian plane"
    def __init__(self, bottom: float, left: float, top: float, right: float):
        "Creation of a rectangle is expensive"
        sleep(0.003*random())  # EXPENSIVE
        assert top >= bottom
        assert right >= left
        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right

    @cache
    def area(self):
        "Suppose that area calculation is expensive"
        sleep(0.005 * random())  # EXPENSIVE
        return (self.top - self.bottom) * (self.right - self.left)

    @cache
    def move(self, vertical: float, horizontal: float):
        "Moving rectangle is expensive"
        sleep(0.003 * random())  # EXPENSIVE
        self.top += vertical
        self.left += vertical
        self.bottom += horizontal
        self.right += horizontal
        return self

    @cache
    def resize(self, vertical: float, horizontal: float):
        "Resizing rectangle is expensive"
        sleep(0.003 * random())  # EXPENSIVE
        self.top = vertical * (self.top-self.bottom) + self.bottom
        self.right = horizontal * (self.right-self.left) + self.left
        return self
