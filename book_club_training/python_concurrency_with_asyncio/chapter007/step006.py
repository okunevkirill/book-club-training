import time
import requests


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


start = time.perf_counter()
urls = ["https://www.example.com" for _ in range(100)]
for _url in urls:
    print(get_status_code(_url))
end = time.perf_counter()
print(f"Выполнение запросов завершено за {end - start:.4f} с")
