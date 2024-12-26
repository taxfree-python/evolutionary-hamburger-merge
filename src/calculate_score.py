import random
from collections import Counter

import buns
import existing_menus
import fillings

BUNS = buns.BUNS
FILLINGS = fillings.FILLINGS
EXISTING_MENUS = existing_menus.EXISTING_MENUS
item_weights = BUNS | FILLINGS


def calc_cost(menu_listA: list, item_weights: dict) -> int:
    dictA = Counter(menu_listA)

    total_cost = 0
    for key in dictA.keys():
        cost = item_weights[key][1]
        total_cost += dictA[key] * cost

    return total_cost


def evaluate_cost(hamburger_sequence: list):
    cost = calc_cost(hamburger_sequence, item_weights)

    return cost


def calc_weighted_diff_distance(
    menu_listA: list, menu_listB: list, item_weights: dict
) -> float:
    dictA = Counter(menu_listA)
    dictB = Counter(menu_listB)

    all_items = set(dictA.keys()) | set(dictB.keys())

    distance = 0.0
    for item in all_items:
        print(dictA)
        print(dictB)
        print(item)
        count_a = dictA[item]
        count_b = dictB[item]
        diff_count = abs(count_a - count_b)
        weight = item_weights[item][0]
        distance += diff_count * weight

    return distance


def evaluate_uniqueness(hamburger_sequence: list) -> float:
    distances = []
    for exist_hamburger_sequence in EXISTING_MENUS:
        dist = calc_weighted_diff_distance(
            hamburger_sequence, exist_hamburger_sequence, item_weights
        )
        distances.append(dist)

    return min(distances)
