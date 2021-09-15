from flask import Flask, redirect, render_template, url_for, request, flash, session, escape, Blueprint

import database as db
import events as ev

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mNdbabQ5#YSxLs76r$72B4g5jFRCeHSQ&KrQzuaChky$UtwH2gm#FTdEhuwfCGwn'

# =======================================================================
# Вспомогающие функции
# =======================================================================
def isUserAdminAuth():
    if 'adminToken' in session:
        if db.isUserAdmin(session['adminToken']):
            return True
        else:
            return False
    else:
        return False

def isUserAuth():
    if 'user' not in session or 'user_token' not in session or 'isGuest' in session:
        return False
    else: 
        return True

def checkAdding():
    if not isUserAuth() and 'isGuest' not in session:
        session['user'] = db.addGuestUser()
        session['isGuest'] = True

def fillBreadCrumbs():
    if 'breadcrumbs' not in session:
        session['breadcrumbs'] = [['', ''], ['', ''], ['', '']]
# =======================================================================
# Роуты и маршруты
# =======================================================================
@app.context_processor
def processValues():
    if 'user' in session:
        return dict(isAuth=isUserAuth(), counters=db.getCounters(session['user']))
    else:
        return dict(isAuth=isUserAuth(), counters=[0, 0])

@app.route('/admin')
def adminPage():
    if isUserAdminAuth():
        data = db.getAllGoods()
        return render_template('admin.html', data=data)
    else:
        return render_template('authAdmin.html')

@app.route('/admin/logout')
def adminLogout():
    if isUserAdminAuth():
        session.pop('adminToken', None)
    
    return redirect('/admin')

@app.route('/admin/auth', methods=['POST'])
def authAdmin():
    if request.method == 'POST':
        if db.authAdmin(request.form['login'], request.form['password']):
            session['adminToken'] = db.getAdminToken(request.form['login'])
        
        return redirect('/admin')
        
    else:
        return redirect('/not_found')

@app.route('/admin/edit/<string:article>')
def adminEditPage(article):
    if isUserAdminAuth():
        data = db.getGoodByID(article)
        return render_template('adminEdit.html', data=data)
    else:
        return redirect('/not_found')

@app.route('/admin/remove/<string:article>')
def adminRemovePage(article):
    if isUserAdminAuth():
        db.removeGoodByID(article)
        return redirect('/admin')
    else:
        return redirect('/not_found')

@app.route('/admin/addNew', methods=['POST'])
def adminAddNewPage():
    if isUserAdminAuth():
        
        data = {  }
        
        if str(request.form['name']).strip() == '':
            data['name'] = 'Не указано'
        else:
            data['name'] = request.form['name']

        if str(request.form['descr']).strip() == '':
            data['descr'] = 'Не указано'
        else:
            data['descr'] = request.form['descr']
            
        if str(request.form['price']).strip() == '':
            data['price'] = 0
        else:
            data['price'] = request.form['price']
            
        if str(request.form['brand']).strip() == '':
            data['brand'] = 'Не указано'
        else:
            data['brand'] = request.form['brand']
            
        if str(request.form['country']).strip() == '':
            data['country'] = 'Не указано'
        else:
            data['country'] = request.form['country']
            
        if str(request.form['material']).strip() == '':
            data['material'] = 'Не указано'
        else:
            data['material'] = request.form['material']
            
        if str(request.form['composition']).strip() == '':
            data['composition'] = 'Не указано'
        else:
            data['composition'] = request.form['composition']
            
        if str(request.form['catalogNum']).strip() == '':
            data['catalogID'] = 0
        else:
            data['catalogID'] = request.form['catalogNum']
            
        if str(request.form['catalogName']).strip() == '':
            data['catalogName'] = 'Не указано'
        else:
            data['catalogName'] = request.form['catalogName']
            
        if str(request.form['filterNum']).strip() == '':
            data['filterID'] = 0
        else:
            data['filterID'] = request.form['filterNum']

        if str(request.form['filterName']).strip() == '':
            data['filterName'] = 'Не указано'
        else:
            data['filterName'] = request.form['filterName']

        db.addNewGood(data)
        return redirect('/admin')
    else:
        return redirect('/not_found')

@app.route('/admin/applyEdit', methods=['POST'])
def adminApplyEdit():
    if isUserAdminAuth():

        data = {  }

        data['article'] = request.form['article']
        
        if str(request.form['name']).strip() == '':
            data['name'] = 'Не указано'
        else:
            data['name'] = request.form['name']

        if str(request.form['descr']).strip() == '':
            data['descr'] = 'Не указано'
        else:
            data['descr'] = request.form['descr']
            
        if str(request.form['price']).strip() == '':
            data['price'] = 0
        else:
            data['price'] = request.form['price']
            
        if str(request.form['brand']).strip() == '':
            data['brand'] = 'Не указано'
        else:
            data['brand'] = request.form['brand']
            
        if str(request.form['country']).strip() == '':
            data['country'] = 'Не указано'
        else:
            data['country'] = request.form['country']
            
        if str(request.form['material']).strip() == '':
            data['material'] = 'Не указано'
        else:
            data['material'] = request.form['material']
            
        if str(request.form['composition']).strip() == '':
            data['composition'] = 'Не указано'
        else:
            data['composition'] = request.form['composition']
            
        if str(request.form['catalogNum']).strip() == '':
            data['catalogID'] = 0
        else:
            data['catalogID'] = request.form['catalogNum']
            
        if str(request.form['catalogName']).strip() == '':
            data['catalogName'] = 'Не указано'
        else:
            data['catalogName'] = request.form['catalogName']
            
        if str(request.form['filterNum']).strip() == '':
            data['filterID'] = 0
        else:
            data['filterID'] = request.form['filterNum']

        if str(request.form['filterName']).strip() == '':
            data['filterName'] = 'Не указано'
        else:
            data['filterName'] = request.form['filterName']

        db.applyEditGood(data)
        return redirect('/admin')
    else:
        return redirect('/not_found')

@app.route('/')
@app.route('/index')
def indexPage():
    session['lastSeenPage'] = '/'
    data = db.getAllCatalogs()
    return render_template('index.html', catalog=data)

@app.route('/gallery')
def galleryPage():
    session['lastSeenPage'] = '/gallery'
    return render_template('gallery.html')

@app.route('/news')
def newsPage():
    session['lastSeenPage'] = '/news'
    return render_template('news.html')

@app.route('/about')

def aboutPage():
    session['lastSeenPage'] = '/about'
    return render_template('about.html')

@app.route('/sales')
def salesPage():
    session['lastSeenPage'] = '/sales'
    return render_template('sales.html')

@app.route('/catalog')
def catalogPage():
    session['lastSeenPage'] = '/catalog'
    data = db.getAllCatalogs()
    fillBreadCrumbs()
    return render_template('catalog.html', catalogType="catalog", catalog=data)
    
@app.route('/catalog/filters/<string:catalog>')
def catalogFiltersPage(catalog):
    session['lastSeenPage'] = '/catalog/filters/' + str(catalog)
    data = db.getAllFiltersFromCatalog(catalog)
    crumbPart = db.getCatalogName(catalog)
    session['breadcrumbs'][0][0] = str(catalog)
    session['breadcrumbs'][0][1] = str(crumbPart)
    fillBreadCrumbs()
    return render_template('catalog.html', catalogType="filter", catalog=data, breadcrumbs=session['breadcrumbs'])

@app.route('/catalog/filters/goods/<string:fltr>')
def catalogFiltersGoodsPage(fltr):
    session['lastSeenPage'] = '/catalog/filters/goods/' + str(fltr)
    data = db.getAllGoodsFromFilter(fltr)
    crumbPart = db.getFilterName(fltr)
    session['breadcrumbs'][1][0] = str(fltr)
    session['breadcrumbs'][1][1] = str(crumbPart)
    fillBreadCrumbs()
    return render_template('catalog.html', catalogType="goods", catalog=data, breadcrumbs=session['breadcrumbs'])

@app.route('/good/<int:article>')
def catalogFiltersGoodsItemPage(article):
    session['lastSeenPage'] = '/good/' + str(article)
    data = db.getGoodByID(article)
    print(data)
    session['breadcrumbs'][0][0] = str(data[10])
    session['breadcrumbs'][0][1] = str(data[11])
    session['breadcrumbs'][1][0] = str(data[12])
    session['breadcrumbs'][1][1] = str(data[13])
    session['breadcrumbs'][2][0] = str(article)
    session['breadcrumbs'][2][1] = str(data[1])
    fillBreadCrumbs()
    return render_template('good.html', data=data, breadcrumbs=session['breadcrumbs'])

@app.route('/profile')
def profilePage():
    return redirect('/orders')

@app.route('/orders')
def ordersPage():
    if isUserAuth():
        session['lastSeenPage'] = '/orders'
        return render_template('orders.html', orders=db.getOrders(session['user']))
    else:
        return redirect(session['lastSeenPage'])

@app.route('/wanted')
def wantedPage():
    checkAdding()
    session['lastSeenPage'] = '/wanted'
    return render_template('wanted.html', data=db.getWantedList(session['user']))

@app.route('/basket')
def basketPage():
    checkAdding()
    session['lastSeenPage'] = '/basket'
    return render_template('basket.html', data=db.getBasketList(session['user']))

@app.route('/register')
def registerPage():
    session['lastSeenPage'] = '/register'
    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_token', None)
    session.pop('user', None)
    session.pop('isGuest', None)
    return redirect('/')

@app.errorhandler(404)
@app.route('/not_found')
def page_not_found(e):
    return render_template("error404.html"), 404

# =======================================================================
# API запросы и т.п.
# =======================================================================

@app.route('/api/addToBasket/<int:article>', methods=['POST', 'GET'])
def apiAddToBasket(article):
    checkAdding()
    db.addToBasket(session['user'], article, request.form['inputAmount'])
    return redirect('/basket')

@app.route('/api/fastAddToBasket/<int:article>', methods=['POST', 'GET'])
def apiFastAddToBasket(article):
    checkAdding()
    db.quickAddToBasket(session['user'], article)
    return redirect(session['lastSeenPage'])

@app.route('/api/fastAddToWanted/<int:article>', methods=['POST', 'GET'])
def apiFastAddToWanted(article):
    checkAdding()
    db.quickAddToWanted(session['user'], article)
    return redirect(session['lastSeenPage'])

@app.route('/api/dropFromWanted/<int:article>', methods=['POST', 'GET'])
def apiDropFromWanted(article):
    checkAdding()
    db.dropFromWanted(session['user'], article)
    return redirect(session['lastSeenPage'])

@app.route('/api/dropFromBasket/<int:article>', methods=['POST', 'GET'])
def apiDropFromBasket(article):
    checkAdding()
    db.dropFromBasket(session['user'], article)
    return redirect(session['lastSeenPage'])

@app.route('/api/registerUser', methods=['POST'])
def apiRegisterUser():
    if request.method == 'POST':
        isEndedWell, errorCode = db.registerUser(request.form)
        if isEndedWell:
            if 'isGuest' in session:
                db.relocateBasketAndWanted(session['user'], request.form['inputLogin'])
                session.pop('isGuest', None)

            session['user'] = request.form['inputLogin']
            session['user_token'] = ev.generateUserToken(request.form['inputLogin'])
            return redirect('/profile')
        else:
            if errorCode == 1:
                flash('Пароли не совпадают!')
            elif errorCode == 2:
                flash('Такой пользователь уже существует!')

            return redirect('/register')
    else:
        return redirect('/not_found')

@app.route('/api/authUser', methods=['POST'])
def apiAuthUser():
    if request.method == 'POST':
        if db.authUser(request.form):
            if session['isGuest']:
                db.relocateBasketAndWanted(session['user'], request.form['inputLogin'])
                session.pop('isGuest', None)

            session['user'] = request.form['inputLogin']
            session['user_token'] = ev.generateUserToken(request.form['inputLogin'])
            return redirect('/profile')
        else:
            return redirect('/')
    else:
        return redirect('/not_found')

@app.route('/api/appendOrder', methods=['POST'])
def apiAppendOrder():
    if request.method == 'POST':
        if isUserAuth():
            choosed = request.form.getlist('goodChoosing')        
            orderGoods = []
            for n in choosed:
                orderGoods.append([n, request.form.get('inputAmount_' + str(n))])

            db.appendOrder(session['user'], orderGoods)
            return redirect('/orders')
        else:
            flash('Для совершения покупки необходима авторизация')
            return redirect(session['lastSeenPage'])

        return redirect('/orders')
    else:
        return redirect('/not_found')

if __name__ == '__main__':
    app.run()