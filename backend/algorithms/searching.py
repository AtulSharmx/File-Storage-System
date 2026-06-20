"""
Search algorithms - written by hand. This is the other half of the DSA
certificate tie-in, alongside sorting.py.

Two different algorithms are used here on purpose, because they solve
two different problems:

1. linear_search   -> for "find files containing X in the name"
                       (partial match, like a normal search box)
                       Time complexity: O(n) - checks every item once.

2. binary_search    -> for "find the exact file named X"
                       Only works on a list that is ALREADY sorted by
                       the same field you're searching on.
                       Time complexity: O(log n) - much faster than
                       linear search on large lists, because it cuts
                       the search space in half every step, the same
                       idea as merge sort.
"""


def linear_search(items, query, key=lambda x: x):
    """
    Scans every item and keeps the ones where `query` appears anywhere
    in the value. Case-insensitive. Good for partial/substring search.
    """
    query = query.lower().strip()
    matches = []

    for item in items:
        value = str(key(item)).lower()
        if query in value:
            matches.append(item)

    return matches


def binary_search_exact(sorted_items, target, key=lambda x: x):
    """
    Looks for an EXACT match in a list that is already sorted ascending
    by `key`. Returns the matching item, or None if not found.

    Repeatedly checks the middle element:
      - if it matches, done
      - if the target is bigger, ignore the left half and search the right
      - if the target is smaller, ignore the right half and search the left
    """
    low = 0
    high = len(sorted_items) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_items[mid])

        if mid_val == target:
            return sorted_items[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None
