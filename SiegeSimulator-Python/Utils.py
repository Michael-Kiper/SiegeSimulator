import math


def angle(p1, p2) -> int:
    x_dist = (p2[0] - p1[0])
    y_dist = (p2[1] - p1[1])
    angle = (math.atan2(y_dist, x_dist) - math.atan2(0, 0)) * 180 / math.pi - 90
    return int(angle)