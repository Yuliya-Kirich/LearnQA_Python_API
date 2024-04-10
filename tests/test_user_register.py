import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    base_url = "https://playground.learnqa.ru/api/user/"

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
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    missing_fields = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]
    data = {
        "username": "user2",
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane@example.com",
        "password": "123"
    }

    @pytest.mark.parametrize("missing_field", missing_fields)
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
