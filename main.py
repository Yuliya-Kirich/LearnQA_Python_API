import requests

name = 'Yuliya'
p_for ='for'
url = f'https://playground.learnqa.ru/api/hello?name={p_for}%20{name}'
response = requests.get('https://playground.learnqa.ru/api/Hello?name={name}', params={'name':'Yuliya', 'for':'for'})
response = requests.get(url)
print(response.text)

