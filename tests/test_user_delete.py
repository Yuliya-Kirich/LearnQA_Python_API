import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserDelete(BaseCase):
    def test_delete_user_wrong_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.delete("https://playground.learnqa.ru/api/user/2", headers=self.get_auth_headers(data=data))

        Assertions.assert_code_status(response, 400)
        expected_message = "Auth token not supplied"
        Assertions.assert_response_content(response, expected_message)

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        self.register_data = {
            "username": "testuser",
            "firstName": "Johntest",
            "lastName": "Testdone",
            "password": "1234",
            "email": email
        }
        self.user_id, self.auth_sid, self.token = self.create_user(**self.register_data)

    def test_delete_user_positive(self):
        response = requests.delete(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                   headers={"Cookie": self.auth_sid})
        Assertions.assert_code_status(response, 400)
        response_get = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id}")
        Assertions.assert_code_status(response_get, 400)

    def test_delete_user_wrong_auth(self):
        register_data = {
            "username": "testuser",
            "firstName": "Johntest",
            "lastName": "Testdone",
            "password": "1234",
            "email": "testuser43356@example.com"
        }
        _, auth_sid, _ = self.create_user(**register_data)

        response = requests.delete(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                   headers={"Cookie": auth_sid})

        Assertions.assert_code_status(response, 400)
        expected_message = "Auth token not supplied"
        Assertions.assert_response_content(response, expected_message)
