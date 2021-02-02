import requests
# список сайтов
site_list = [
    'google.com',
    'habr.com',
    'openspace.ru',
    'lia.chat',
    'film.ru'
]
# количество запросов
req_num = 10

for i in site_list:
    path = 'http://' + i   # путь к сайту
    print(path) 
    # запись ответов в файл с выводом в консоль
    with open(i + '.log', 'w') as f:
        for j in range(req_num):
            response = requests.get(path)
            ans = ''.join([str(j), ': ', str(response.status_code), '\n'])
            print(ans)
            f.write(ans)

print('DDos complete!')
