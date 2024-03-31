import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
methods = ["GET", "POST", "PUT", "DELETE"]
response = requests.get(url, params={'method': 'HEAD'})

def send_request(url, method=None, data=None):
    errors = []
    try:
        if method not in ["GET", "POST", "PUT", "DELETE"]:
            errors.append(f"Неподдерживаемый метод: {method}")
        if method == "GET":
            response = requests.get(url, params=data)
        else:
            response = requests.request(method, url, data=data)
        return response
    except Exception as e:
        errors.append(f"Ошибка при выполнении запроса: {e}")
        for error in errors:
            print(error)
        return None


def test_incorrect_combinations():
    print("\n1. Запрос без параметра method:")
    response = requests.request('GET', url)
    print("Статус код:", response.status_code)
    print("Текст ответа:", response.text)


def test_noname_method():
    print("\n2. Запрос с неизвестным методом (HEAD):")
    response = send_request(url, "HEAD", data={"method": "HEAD"})
    print("Статус код:", response.status_code)
    print("Текст ответа:", response.text)


def test_true_method():
    print("\n3. Запрос с правильным значением method (GET):")
    response = send_request(url, "GET", data={"method": "GET"})
    print("Статус код:", response.status_code)
    print("Текст ответа:", response.text)


def test_combination():

    print("\n4. Поиск несоответствий в сочетаниях:")
    for method in methods:
        for every_m in methods:
            data = {"method": every_m}
            print(f"\nТип запроса: {method}, Параметр method: {every_m}")
            response = send_request(url, method, data=data)
            if response.status_code == 200:
                print("Сервер отвечает, как будто все в порядке.")
                print("Статус код:", response.status_code)
                print("Текст ответа:", response.text)
            else:
                print("Сервер не отвечает, как мы ожидали.")
                print("Статус код:", response.status_code)
                print("Текст ответа:", response.text)
