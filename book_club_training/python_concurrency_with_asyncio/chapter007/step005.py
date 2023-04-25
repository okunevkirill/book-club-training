import time
import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


start = time.perf_counter()

with ThreadPoolExecutor() as pool:
    urls = ["https://www.example.com" for _ in range(100)]
    results = pool.map(get_status_code, urls)
    for result in results:
        print(result)
    end = time.perf_counter()
    print(f"Выполнение запросов завершено за {end - start:.4f} с")
