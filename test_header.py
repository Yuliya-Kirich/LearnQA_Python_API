import pytest
import requests

def test_homework_header():
 url = "https://playground.learnqa.ru/api/homework_header"
 response = requests.get(url)
 print(response.headers)
 assert 'x-secret-homework-header' in response.headers, "Заголовок 'x-secret-homework-header' не установлен в ответе"
 expected_value = "Some secret value"
 actual_value = response.headers.get('x-secret-homework-header')
 assert actual_value == expected_value, f"У заголовока x-secret-homework-header отсутствует ожидаемое значение {expected_value}"
