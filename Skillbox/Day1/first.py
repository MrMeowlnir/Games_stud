import random

def goodgen(length):
    
    # 1 задать алфавит
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = alphabet + alphabet.upper() + '0123456789' + '!@#$%^&*()'
    # 2 сгенерировать символ из алфавита случайно
    # 3 повторить операцию 2 length раз
    # 4 склеить в строку выбранные символы и выдать результат
    '''
    password = ''
    for i in range(length):
        password += random.choice(alphabet)

    #password = [random.choice(alphabet) for i in range(length)]
    return password
    '''
    return ''.join(random.choices(alphabet, k = length))

popular_pass = [
    '123456',
    '12345',
    'admin',
    'qwerty'
]

def badgen():
    # использовать popular_pass 
    #
    #
    #



password = goodgen(10)
print(password)
