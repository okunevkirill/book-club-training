import functools
from typing import Dict
from collections import Counter


def map_frequency(text: str) -> Dict[str, int]:
    return dict(Counter(text.split()))


def merge_dictionaries_1(
    first: Dict[str, int], second: Dict[str, int]
) -> Dict[str, int]:
    return {
        key: first.get(key, 0) + second.get(key, 0)
        for key in first.keys() | second.keys()
    }


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    return dict(Counter(first) + Counter(second))


def merge_dictionaries_old(
    first: Dict[str, int], second: Dict[str, int]
) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


lines = [
    "I know what I know",
    "I know that I know",
    "I don't know much",
    "They don't know much",
]

mapped_results = [map_frequency(line) for line in lines]

for result in mapped_results:
    print(result)

print(functools.reduce(merge_dictionaries, mapped_results))
