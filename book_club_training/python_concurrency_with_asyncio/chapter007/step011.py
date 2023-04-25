from threading import RLock, Thread
from typing import List


list_lock = RLock()  # Объект с возможностью повторной блокировки
# list_lock = Lock()  # Объект без возможности повторного блокирования в одном потоке


def sum_list(int_list: List[int]) -> int:
    print("Ожидание блокировки...")
    with list_lock:
        print("Блокировка захвачена.")
        if len(int_list) == 0:
            print("Суммирование завершено.")
            return 0
        else:
            head, *tail = int_list
            print("Суммируется остаток списка.")
            return head + sum_list(tail)


thread = Thread(target=sum_list, args=([1, 2, 3, 4],))
thread.start()
thread.join()
