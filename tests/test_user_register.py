import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUserRegister(BaseCase):
    base_url = "https://playground.learnqa.ru/api/user/"

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            "username": "user1",
            "firstName": "John",
            "lastName": "Doe",
            "email": self.email,
            "password": "123"
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_incorrect_email(self):
        email = 'incorrectemail.com'
        data = {
            "username": "user1",
            "firstName": "John",
            "lastName": "Doe",
            "email": email,
            "password": "123"
        }
        response = requests.post(self.base_url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("missing_field", [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ])
    def test_create_user_missing_field(self, missing_field):
        data = {
            "username": "user2",
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com",
            "password": "123"
        }
        del data[missing_field]
        response = requests.post(self.base_url, data=data)
        Assertions.assert_code_status(response, 400)

    def test_create_user_with_short_name(self):
        data = {
            "username": "a",
            "firstName": "A",
            "lastName": "Doe",
            "email": "shortname@example.com",
            "password": "123"
        }
        response = requests.post(self.base_url, data=data)
        Assertions.assert_code_status(response, 400)

    def test_create_user_with_long_name(self):
        long_name = "a" * 251
        data = {
            "username": long_name,
            "firstName": "LongName",
            "lastName": "Doe",
            "email": "longname@example.com",
            "password": "123"
        }
        response = requests.post(self.base_url, data=data)
        Assertions.assert_code_status(response, 400)
