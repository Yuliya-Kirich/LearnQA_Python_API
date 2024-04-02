import pytest
import requests

def test_homework_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    print(dict(response.cookies))
    assert 'HomeWork' in response.cookies, "Cookie HomeWork отсутствует в ответе"
    assert response.cookies['HomeWork'] == 'hw_value', "Для cookie HomeWork отсутствует значение hw_value"
