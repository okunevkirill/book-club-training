import requests

# Веб-запрос ограничен производительностью ввода-вывода
response = requests.get("https://www.google.ru/")
items = response.headers.items()
# Обработка ответа ограничена быстродействием процессора
headers = [f"{key}: {header}" for key, header in items]
# Конкатенация строк ограничена быстродействием процессора
formatted_headers = "\n".join(headers)
with open("headers.txt", "w") as file:
    # Запись на диск ограничена производительностью ввода-вывода
    file.write(formatted_headers)
