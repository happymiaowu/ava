import math


def dist(start_cord, end_cord):
    return math.sqrt((start_cord[0] - end_cord[0]) ** 2 + (start_cord[1] - end_cord[1]) ** 2)


def count_next_cord(start_cord, end_cord, speed):
    d = dist(start_cord, end_cord)

    if d <= speed:
        return end_cord

    during = d / speed
    return ((end_cord[0] - start_cord[0]) / during + start_cord[0], (end_cord[1] - start_cord[1]) / during + start_cord[1])

def check_cord_valid(cord, empty_cord):
    return cord in empty_cord


def is_same_team(hive_id1, hive_id2):
    return hive_id1.split('_')[0] == hive_id2.split('_')[0]