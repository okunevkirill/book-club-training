from threading import RLock
from typing import List


class IntListThreadsafe:
    def __init__(self, wrapped_list: List[int]):
        self._lock = RLock()
        self._inner_list = wrapped_list

    @property
    def inner_list(self):
        return self._inner_list

    def indices_of(self, to_find: int) -> List[int]:
        with self._lock:
            enumerator = enumerate(self._inner_list)
            return [index for index, value in enumerator if value == to_find]

    def find_and_replace(self, to_replace: int, replace_with: int) -> None:
        with self._lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self._inner_list[index] = replace_with


threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
print(threadsafe_list.inner_list)
threadsafe_list.find_and_replace(1, 3)
threadsafe_list.find_and_replace(2, 5)
print(threadsafe_list.inner_list)
