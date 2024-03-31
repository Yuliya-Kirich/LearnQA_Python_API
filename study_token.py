import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

def create_job():
    response = requests.get(url)
    response_json = response.json()
    seconds = response_json.get('seconds')
    print(f"До создания задачи осталось {seconds} секунд")
    return response_json

def check_job_status():
    information = create_job()
    token = information.get('token')
    payload = {'token': token}

    response = requests.get(url, params=payload)
    status = response.json().get('status')
    print(f"Текущий статус: {status}")

    if status == "Job is NOT ready":
        print("Задача еще не готова. Ожидание...")
        time.sleep(information.get('seconds'))
        response = requests.get(url, params=payload)
        status = response.json().get('status')
        print(f"Обновленный статус: {status}")

    if status == "Job is ready":
        result = response.json().get('result')
        print("Задача выполнена. Результат:", result)
    else:
        print("Произошла ошибка. Подробности:", response.json())

check_job_status()