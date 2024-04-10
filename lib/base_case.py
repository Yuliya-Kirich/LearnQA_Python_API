import json.decoder
import requests
from requests import Response


class BaseCase:
    base_url = "https://playground.learnqa.ru/api/user/"

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find cookie with the {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f'Response JSON doesn\'t have key \'{name}\''
        return response_as_dict[name]


    def create_user(self, username, firstName, lastName, email, password):
        response = requests.post(f"{self.base_url}", data={
            "username": username,
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": password
            }
                                 )

        assert response.status_code == 200, f"Failed to create user. Status code: {response.status_code}"
        response_dict = response.json()
        user_id = response_dict['id']
        response_login = requests.post(f"{self.base_url}login", data={"email": email, "password": password})
        assert response_login.status_code == 200, f"Failed to login user. Status code: {response_login.status_code}"
        auth_sid = response.cookies.get("auth_sid")
        token = response.headers.get("x-csrf-token")

        return user_id, auth_sid, token

    def get_auth_headers(self, data=None):
        if data is None:
            data = {}
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        assert response.status_code == 200, f"Unexpected status code {response.status_code} when logging in"
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        headers = {"x-csrf-token": token, "Cookie": auth_sid}
        return headers
