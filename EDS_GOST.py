import random
from sympy import *
from hashlib import sha256

def gen_key():
    p = 0
    q = 0
    a = 1
    while not isprime(q):
        q = random.randint(2 ** 254, 2 ** 256)
    print('q =', q)
    m = 2 ** 509 // q
    while not isprime(p):
        m += 1
        p = q * m + 1
    print('p =', p)
    while a == 1:
        e = random.randint(1, p - 1)
        # print('e =', e)
        a = pow(e, m, p)
        print('a =', a)

    x = random.randint(1, q)
    y = pow(a, x, p)

    print('x =', x, '\ny =', y)

    file = open('Открытый ключ.txt', 'w', encoding='UTF-8')
    file.write(str(y) + '\n' + str(p) + '\n' + str(q) + '\n' + str(a))
    file.close()
    file = open('Закрытый ключ.txt', 'w', encoding='UTF-8')
    file.write(str(x) + '\n' + str(p) + '\n' + str(q) + '\n' + str(a))
    file.close()

def Hash():
    file = open('Л2-Митюшкина .docx', 'rb')
    f = file.read()
    file.close()
    hash_object = int(sha256(f).hexdigest(), 16)
    print('Хеш:', format(hash_object, 'x'))
    return hash_object

"""Подпись документа"""
def Sign():
    hash_object = Hash()
    file = open('Закрытый ключ.txt', 'r', encoding='UTF-8')
    x = int(file.readline())
    p = int(file.readline())
    q = int(file.readline())
    a = int(file.readline())
    file.close()

    r = 0
    while r == 0:
        k = random.randint(1, q)
        r = pow(a, k, p) % q
    if hash_object % q == 0:
        hash_object = 1
    s = (x * r + k * hash_object) % q
    print('r=', r, '\ns=', s)

    file = open('Подпись.txt', 'w')
    file.write(str(r) + '\n' + str(s))
    file.close()

"""Проверка документа"""
def Verification():
    hash_object = Hash()
    file = open('Открытый ключ.txt', 'r', encoding='UTF-8')
    y = int(file.readline())
    p = int(file.readline())
    q = int(file.readline())
    a = int(file.readline())
    file.close()

    file = open('Подпись.txt', 'r')
    r = int(file.readline())
    s = int(file.readline())
    file.close()

    v = pow(hash_object, q - 2, q)
    z1 = (s * v) % q
    z2 = ((q - r) * v) % q
    u = ((pow(a, z1, p) * pow(y, z2, p)) % p) % q

    print('r=', r, '\nu=', u)

    if r == u:
        print('Подпись действительна!')
    else:
        print('Подпись недействительна!')

actions = int(input('Генерация новых ключей:'))
if actions == 1:
    gen_key()
    Sign()
    Verification()
else:
    Verification()