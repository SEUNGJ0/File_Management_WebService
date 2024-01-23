import requests
 
url = "http://127.0.0.1:8000/api/auth"

response = requests.post(url, data={'username':'kuksj0312@naver.com', 'password':'1562'})
myToken = response.json()['token']

header = {'Authorization': 'Token '+myToken}
response = requests.get('http://127.0.0.1:8000/api/users', headers=header)
print(response.text)