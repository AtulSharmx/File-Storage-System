"""
Quick manual test - run this with: python test_algorithms.py
Just checks that merge_sort, linear_search, and binary_search_exact
are actually working correctly before we wire them into the API.
"""

from algorithms.sorting import merge_sort
from algorithms.searching import linear_search, binary_search_exact

files = [
    {"name": "report.pdf", "size": 500, "last_modified": "2026-06-10"},
    {"name": "notes.txt", "size": 20, "last_modified": "2026-06-15"},
    {"name": "diagram.png", "size": 1200, "last_modified": "2026-06-01"},
    {"name": "data.csv", "size": 80, "last_modified": "2026-06-17"},
]

print("--- Sort by name (A-Z) ---")
for f in merge_sort(files, key=lambda f: f["name"]):
    print(f["name"])

print("\n--- Sort by size (largest first) ---")
for f in merge_sort(files, key=lambda f: f["size"], reverse=True):
    print(f["name"], f["size"])

print("\n--- Search for 'da' (should match only data.csv) ---")
for f in linear_search(files, "da", key=lambda f: f["name"]):
    print(f["name"])

print("\n--- Binary search for exact name 'notes.txt' ---")
sorted_by_name = merge_sort(files, key=lambda f: f["name"])
result = binary_search_exact(sorted_by_name, "notes.txt", key=lambda f: f["name"])
print(result["name"] if result else "Not found")

print("\nAll checks ran. Compare the output above with what you'd expect manually.")
