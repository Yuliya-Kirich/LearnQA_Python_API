import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
count_response = len(response.history)
final_url = response.history[-1].url
print(f"Редиректов от изначальной точки назначения до итоговой - {count_response}")
print(f"Итоговый url - {final_url}")