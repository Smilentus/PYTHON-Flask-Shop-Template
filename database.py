import sqlite3

import events as ev

def connect():
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    return conn, cursor

def close(conn):
    conn.close()

def getAllCatalogs():
    conn, cursor = connect()

    data = cursor.execute("SELECT catalogID, catalogName FROM goods GROUP BY catalogID").fetchall()

    close(conn)

    return data

def getAllFiltersFromCatalog(catalog):
    conn, cursor = connect()

    data = cursor.execute("SELECT filterID, filterName FROM goods WHERE catalogID = ? GROUP BY filterID", (catalog, )).fetchall()

    close(conn)

    return data

def getAllGoodsFromFilter(catalogFilter):
    conn, cursor = connect()

    data = cursor.execute("SELECT article, name, price, discount, image_path FROM goods WHERE filterID = ?", (catalogFilter, )).fetchall()

    close(conn)
    
    return data

def getGoodByID(article):
    conn, cursor = connect()

    data = cursor.execute("SELECT * FROM goods WHERE article = ?", (article, )).fetchall()[0]

    close(conn)

    return data

def isUserExist(user_login):
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM users WHERE user_Email = ?", (user_login,)).fetchall()
    close(conn)
    if len(data) > 0:
        return True
    else:
        return False

def getUserIDByLogin(user):
    conn, cursor = connect()
    userID = cursor.execute("SELECT user_ID FROM users WHERE user_Email = ?", (user, )).fetchall()[0][0]
    close(conn)
    return userID

def getUserDataByLogin(user_login):
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM users WHERE user_Email = ?", (user_login,)).fetchall()[0]
    close(conn)
    return data

def getUserDataByID(user_ID):
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM users WHERE user_ID = ?", (user_ID,)).fetchall()
    close(conn)

def isWantedExist(user, article):
    user_ID = getUserIDByLogin(user)
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM wanted WHERE user_ID = ? AND good_Article = ?", (user_ID, article)).fetchall()
    close(conn)
    if len(data) > 0:
        return True
    else:
        return False

def isBasketExist(user, article):
    user_ID = getUserIDByLogin(user)
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM basket WHERE user_ID = ? AND good_Article = ?", (user_ID, article)).fetchall()
    close(conn)
    if len(data) > 0:
        return True
    else:
        return False

def quickAddToBasket(user, article):
    if not isBasketExist(user, article):
        addToBasket(user, article, 1)

def quickAddToWanted(user, article):
    if not isWantedExist(user, article):
        user_ID = getUserIDByLogin(user)
        conn, cursor = connect()
        cursor.execute("INSERT INTO wanted (user_ID, good_Article) VALUES (?, ?)", (user_ID, article))
        conn.commit()
        close(conn)

def addToBasket(user, article, amount):
    user_ID = getUserIDByLogin(user)
    conn, cursor = connect()
    cursor.execute("INSERT INTO basket (user_ID, good_Article, good_Amount) VALUES (?, ?, ?)", (user_ID, article, amount))
    conn.commit()
    close(conn)

def authUser(formData):
    login = formData['inputLogin']
    password = formData['inputPassword']

    if isUserExist(login):
        userData = getUserDataByLogin(login)
        if ev.hashPassword(password) == userData[4]:
            return True
        else:
            return False
    else:
        return False

def registerUser(formData):
    login = formData['inputLogin']
    password = formData['inputPassword']
    repeatPassword = formData['inputRepeatPassword']
    fullName = formData['inputFullName']
    phone = formData['inputPhone']

    if isUserExist(login):
        return False, 2

    if password != repeatPassword:
        return False, 1

    hPass = ev.hashPassword(password)
    
    conn, cursor = connect()
    cursor.execute("INSERT INTO users (user_Name, user_Phone, user_Email, user_Password) VALUES (?, ?, ?, ?)", (fullName, phone, login, hPass))
    conn.commit()
    close(conn)

    return True, 0

def addGuestUser():
    userLogin = ev.generateUserLogin()
    
    conn, cursor = connect()
    cursor.execute("INSERT INTO users (user_Email) VALUES (?)", (userLogin, ))
    conn.commit()
    close(conn)

    return userLogin

def getWantedList(user_Login):
    user_ID = getUserIDByLogin(user_Login)
    conn, cursor = connect()
    data = cursor.execute("SELECT user_ID, article, name, image_path, price, discount FROM wanted JOIN goods ON article = good_Article WHERE user_ID = ?", (user_ID, )).fetchall()
    close(conn)
    return data

def getBasketList(user_Login):
    user_ID = getUserIDByLogin(user_Login)
    conn, cursor = connect()
    data = cursor.execute("SELECT user_ID, good_Article, good_Amount, name, image_path, price, discount FROM basket JOIN goods ON article = good_Article WHERE user_ID = ?", (user_ID, )).fetchall()
    close(conn)
    return data

def getCounters(user_Login):
    user_ID = getUserIDByLogin(user_Login)
    conn, cursor = connect()
    wantedCounter = cursor.execute("SELECT * FROM wanted WHERE user_ID = ?", (user_ID, )).fetchall()
    basketCounter = cursor.execute("SELECT * FROM basket WHERE user_ID = ?", (user_ID, )).fetchall()
    close(conn)

    return [len(wantedCounter), len(basketCounter)]

def dropFromWanted(user_login, article):
    user_ID = getUserIDByLogin(user_login)
    conn, cursor = connect()
    cursor.execute("DELETE FROM wanted WHERE user_ID = ? AND good_Article = ?", (user_ID, article))
    conn.commit()
    close(conn)

def dropFromBasket(user_login, article):
    user_ID = getUserIDByLogin(user_login)
    conn, cursor = connect()
    cursor.execute("DELETE FROM basket WHERE user_ID = ? AND good_Article = ?", (user_ID, article))
    conn.commit()
    close(conn)

def relocateBasketAndWanted(fromUser, toUser):
    fromUserID = getUserIDByLogin(fromUser)
    toUserID = getUserIDByLogin(toUser)

    conn, cursor = connect()
    cursor.execute("UPDATE basket SET user_ID = ? WHERE user_ID = ?", (toUserID, fromUserID))
    cursor.execute("UPDATE wanted SET user_ID = ? WHERE user_ID = ?", (toUserID, fromUserID))
    cursor.execute("DELETE FROM users WHERE user_ID = ?", (fromUserID, ))
    conn.commit()
    close(conn)

def getOrders(userLogin):
    user_ID = getUserIDByLogin(userLogin)
    conn, cursor = connect()
    query = cursor.execute("SELECT o.order_ID, o.order_Token, o.order_Status, o.order_TotalPrice, og.good_Article, og.good_Amount, og.good_Price FROM orders o JOIN order_goods og ON og.order_ID = o.order_ID WHERE o.user_ID = ?", (user_ID, )).fetchall()
    data = []
    for item in query:
        index = -1
        for x in range(len(data)):
            if data[x]['order'] == str(item[1]):
                index = x
                break
        if index == -1:
            data.append( { 'order': str(item[1]), 'status': item[2], 'totalPrice': item[3], 'goods': [] } )

        good = cursor.execute("SELECT article, name, image_path FROM goods WHERE article = ?", (item[4], )).fetchone()
        data[index]['goods'].append([good[0], good[1], good[2], item[6], item[5], int(item[5]) * int(item[6])])

    close(conn)
    return data

def appendOrder(userLogin, orderData):
    user_ID = getUserIDByLogin(userLogin)
    token = ev.generateOrderToken()
    conn, cursor = connect()
    # Добавляем ордер
    cursor.execute("INSERT INTO orders (user_ID, order_Status, order_Token) VALUES (?, ?, ?)", (user_ID, "processing", token))
    order_ID = cursor.execute("SELECT order_ID FROM orders WHERE user_ID = ? AND order_Token = ?", (int(user_ID), token)).fetchall()[0][0]
    # Добавляем товары в ордер и считаем общую сумму
    total = 0
    for item in orderData:
        goodPrice = cursor.execute("SELECT price FROM goods WHERE article = ?", (item[0], )).fetchone()[0]
        total += goodPrice * int(item[1])
        cursor.execute("INSERT INTO order_goods (order_ID, good_Article, good_Amount, good_Price) VALUES (?, ?, ?, ?);", (int(order_ID), int(item[0]), int(item[1]), goodPrice))
        cursor.execute("DELETE FROM basket WHERE good_Article = ? AND user_ID = ?", (int(item[0]), int(user_ID)))
    cursor.execute("UPDATE orders SET order_TotalPrice = ? WHERE order_Token = ?", (total, token))
    conn.commit()
    close(conn)

def setOrderStatus(order_ID, status):
    conn, cursor = connect()
    cursor.execute("UPDATE orders SET order_Status = ? WHERE order_ID = ?", (status, order_ID))
    conn.commit()
    close(conn)
    
def getFilterName(fltr):
    conn, cursor = connect()
    data = cursor.execute("SELECT filterName FROM goods WHERE filterID = ?", (fltr, )).fetchone()[0]
    close(conn)
    return data

def getCatalogName(catalog):
    conn, cursor = connect()
    data = cursor.execute("SELECT catalogName FROM goods WHERE catalogID = ?", (catalog, )).fetchone()[0]
    close(conn)
    return data

# ========================================================
#                     ADMINISTARTION
# ========================================================

def isUserAdmin(admin_token):
    conn, cursor = connect()
    user = cursor.execute("SELECT admin_Token FROM admins WHERE admin_Token = ?", (admin_token, )).fetchall()
    close(conn)

    if len(user) > 0:
        if user[0][0] == admin_token:
            return True
        else:
            return False
    else:
        return False

def addAdmin(login, password):
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM admins").fetchall()
    admin_ID = 0
    if len(data) == 0:
        admin_ID = 0
    else:
        admin_ID = data[0][0] + 1

    admin_Login = login
    admin_Password = password
    
    hash_Password = ev.hashPassword(admin_Password)
    admin_Token = ev.generateAdminToken(admin_ID, admin_Login, hash_Password)
    cursor.execute("INSERT INTO admins (admin_ID, admin_Login, admin_Password, admin_Token) VALUES (?, ?, ?, ?);", (admin_ID, admin_Login, hash_Password, admin_Token))
    conn.commit()
    close(conn)

def authAdmin(admin_Login, admin_Password):
    conn, cursor = connect()
    user = cursor.execute("SELECT admin_Password FROM admins WHERE admin_Login = ?", (admin_Login, )).fetchall()
    close(conn)

    if len(user) == 0:
        return False

    hashPass = ev.hashPassword(admin_Password)
    if user[0][0] == hashPass:
        return True
    else:
        return False

def getAdminToken(admin_Login):
    conn, cursor = connect()
    data = cursor.execute("SELECT admin_Token FROM admins WHERE admin_Login = ?", (admin_Login, )).fetchone()
    close(conn)

    if len(data) > 0:
        return data[0]
    else:
        return None

def removeGoodByID(article):
    conn, cursor = connect()
    cursor.execute("DELETE FROM goods WHERE article = ?", (article, ))
    conn.commit()
    close(conn)

def applyEditGood(data):
    conn, cursor = connect()
    cursor.execute("UPDATE goods SET name = ?, description = ?, price = ?, brand = ?, material = ?, country = ?, composition = ?, catalogID = ?, catalogName = ?, filterID = ?, filterName = ? WHERE article = ?", (data['name'], data['descr'], data['price'], data['brand'], data['material'], data['country'], data['composition'], data['catalogID'], data['catalogName'], data['filterID'], data['filterName'], data['article']))
    conn.commit()
    close(conn)

def addNewGood(data):
    conn, cursor = connect()
    lastArticle = cursor.execute("SELECT article FROM goods").fetchall()
    if len(lastArticle) > 0:
        lastArticle = lastArticle[len(lastArticle) - 1][0] + 1
    else:
        lastArticle = 1
    cursor.execute("INSERT INTO goods (name, description, price, brand, material, country, composition, catalogID, catalogName, filterID, filterName, image_path, discount, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['name'], data['descr'], data['price'], data['brand'], data['material'], data['country'], data['composition'], data['catalogID'], data['catalogName'], data['filterID'], data['filterName'], lastArticle, 0, 'Не указано'))
    conn.commit()
    close(conn)

def getAllGoods():
    conn, cursor = connect()
    data = cursor.execute("SELECT * FROM goods").fetchall()
    close(conn)
    return data