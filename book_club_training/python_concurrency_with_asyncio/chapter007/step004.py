import requests


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


_url = "https://www.example.com"
print(get_status_code(_url))
print(get_status_code(_url))
