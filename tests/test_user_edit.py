import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import allure


class TestUserEdit(BaseCase):
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        self.register_data = {
            "username": "testuser",
            "firstName": "John",
            "lastName": "Testdone",
            "password": "123",
            "email": email
        }
        self.user_id, self.auth_sid, self.token = self.create_user(**self.register_data)

        another_email = f"another{random_part}@{domain}"
        self.another_user_data = {
            "username": "anotheruser",
            "firstName": "Alice",
            "lastName": "Doe",
            "email": another_email,
            "password": "123"
        }

    @allure.epic("User Management")
    @allure.feature("User Editing")
    @allure.story("Editing User Information")
    @allure.title("Test to edit user information without authentication")
    def test_edit_not_auth(self):
        new_data = {"firstName": "Jane"}
        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}", data=new_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Auth token not supplied")

    @allure.epic("User Management")
    @allure.feature("User Editing")
    @allure.story("Editing User Information")
    @allure.title("Test to edit user information as another user")
    def test_edit_as_another_user(self):
        _, _, another_user_token = self.create_user(**self.another_user_data)
        new_data = {"firstName": "Jane"}
        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}", data=new_data,
                                headers={"x-csrf-token": another_user_token},
                                cookies={"auth_sid": self.auth_sid})
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Auth token not supplied")

    @allure.epic("User Management")
    @allure.feature("User Editing")
    @allure.story("Editing User Information")
    @allure.title("Test to edit user email without @ symbol")
    def test_edit_email_without_at(self):
        new_data = {"email": "testuserexample.com"}
        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}", data=new_data,
                                headers={"x-csrf-token": self.token},
                                cookies={"auth_sid": self.auth_sid})
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Auth token not supplied")

    @allure.epic("User Management")
    @allure.feature("User Editing")
    @allure.story("Editing User Information")
    @allure.title("Test to edit user first name to a very short value")
    def test_edit_to_short_firstName(self):
        new_data = {"firstName": "J"}
        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}", data=new_data,
                                headers={"x-csrf-token": self.token},
                                cookies={"auth_sid": self.auth_sid})
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Auth token not supplied")
