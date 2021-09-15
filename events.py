import hashlib
import random

import database as db

# Не меняй это, иначе пользователи не смогут авторизоваться
SALT = 'H3e0()=W0wxfU[Yzfd8EJeAm6kfTJ|r&'

def hashPassword(password):
    h1 = hashlib.md5(str(password).encode('utf-8'))
    h2 = hashlib.md5(str(SALT).encode('utf-8'))
    gen = h1.hexdigest() + h2.hexdigest()
    return gen

def generateUserToken(user_login):
    if (db.isUserExist(user_login)):
        user_id = db.getUserIDByLogin(user_login)
        h1 = hashlib.md5(str(user_id).encode('utf-8'))
        h2 = hashlib.md5(str(user_login).encode('utf-8'))
        token = h1.hexdigest() + h2.hexdigest()
        return token
    else:
        return "None"

def checkUserTokens(user_token, user_login):
    if db.isUserExist(user_login):
        token = generateUserToken(user_login)
        
        if token == user_token:
            return True
        else:
            return False
    else:
        return False

def generateUserLogin():
    eng = 'abcdefghijklmnopqrstyvwxyz'

    login = 'guest_'

    for ch in range(10):
        login += eng[random.randint(0, len(eng) - 1)]
    
    login += '_'

    for n in range(10):
        login += str(random.randint(0, 10))

    return login

def generateOrderToken():
    token = ''
    for n in range(12):
        token += str(random.randint(0, 10))

    return token

def generateAdminToken(admin_ID, admin_Login, admin_Password):
    token = ''

    h1 = hashlib.md5(str(admin_ID).encode('utf-8'))
    h2 = hashlib.md5(str(admin_Login).encode('utf-8'))
    h3 = hashlib.md5(str(admin_Password).encode('utf-8'))

    token = h1.hexdigest() + h2.hexdigest() + h3.hexdigest()

    return token