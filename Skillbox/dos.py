import requests

for i in range(200):
    response = requests.get('https://www.google.com/')
    print(i,' : ',response.status_code)

