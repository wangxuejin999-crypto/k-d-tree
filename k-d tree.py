from typing import List
from collections import namedtuple
import time
import sys

sys.setrecursionlimit(2000)


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):
    """
    location: Point
    left: Node
    right: Node
    """

    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0

    def insert(self, p: List[Point]):
        """insert a list of points"""
        for point in p:
            self._root = self._insert(self._root, point, 0)
        self._n += len(p)

    def _insert(self, node: Node, point: Point, depth: int) -> Node:
        if node is None:
            return Node(point, None, None)
        if node.location == point:
            return node
        dimension = depth % len(point)
        if point[dimension] < node.location[dimension]:
            node = node._replace(left=self._insert(node.left, point, depth + 1))
        else:
            node = node._replace(right=self._insert(node.right, point, depth + 1))
        return node

    def range(self, rectangle: Rectangle) -> List[Point]:
        """range query"""
        """range query for all points within the given rectangle"""
        return self._range(self._root, rectangle, 0)


    def _range(self, node: Node, rectangle: Rectangle, depth: int) -> List[Point]:
        if node is None:
            return []
        points = []
        if rectangle.is_contains(node.location):
            points.append(node.location)
        dimension = depth % len(node.location)
        if node.left is not None and rectangle.lower[dimension] <= node.location[dimension]:
            points.extend(self._range(node.left, rectangle, depth + 1))
        if node.right is not None and rectangle.upper[dimension] >= node.location[dimension]:
            points.extend(self._range(node.right, rectangle, depth + 1))
        return points


def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()
