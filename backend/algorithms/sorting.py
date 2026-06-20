"""
Sorting algorithm - written by hand, not using Python's built-in sort()
or sorted(). This is the direct link back to the "Introduction to Sorting
Algorithms" and "Basics of Data Structures and Algorithms" certificates.

Algorithm used: Merge Sort
Time complexity: O(n log n) in all cases
Space complexity: O(n)

How it works (plain language):
1. Split the list in half, then split each half in half again, and so on,
   until you're left with pieces of size 1 (a list of 1 item is already sorted).
2. Then merge those tiny pieces back together two at a time, always placing
   the smaller item first. Each merge step produces a bigger sorted list.
3. Keep merging until the whole list is back together, fully sorted.

This is more efficient than something like Bubble Sort (O(n^2)) because it
keeps cutting the problem in half instead of comparing every pair of items.
"""


def merge_sort(items, key=lambda x: x, reverse=False):
    """
    Sorts a list of items and returns a NEW sorted list (original untouched).

    items:   list of things to sort (e.g. list of file-info dictionaries)
    key:     function that pulls out the value to compare
             e.g. key=lambda f: f["size"]  -> sorts by file size
    reverse: True for descending order, False for ascending
    """
    if len(items) <= 1:
        return items[:]

    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key, reverse)
    right_half = merge_sort(items[mid:], key, reverse)

    return _merge(left_half, right_half, key, reverse)


def _merge(left, right, key, reverse):
    """Merges two already-sorted lists into one sorted list."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key(left[i])
        right_val = key(right[j])

        take_left = (left_val <= right_val) if not reverse else (left_val >= right_val)

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # whichever side still has leftover items, tack them on (already sorted)
    result.extend(left[i:])
    result.extend(right[j:])
    return result
