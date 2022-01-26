from flask import Flask, session, app
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from datetime import datetime, timedelta
import pytz

#app 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)
db = SQLAlchemy(app)

#flask login
login_manager = LoginManager()
login_manager.init_app(app)

#user table
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    authority = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable=False)

#store table
class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(20), nullable=False)
    rank = db.Column(db.String(15), nullable=False)
    pref = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(100))
    store_area = db.Column(db.String(200))
    station = db.Column(db.String(200))
    time = db.Column(db.String(50))
    concept = db.Column(db.String(50))
    age = db.Column(db.String(100))
    salary = db.Column(db.String(400), nullable=False)
    nomination = db.Column(db.String(50))
    guarantee = db.Column(db.String(50))
    face = db.Column(db.String(20))
    dormitory = db.Column(db.String(20))
    sundry = db.Column(db.String(50))
    back = db.Column(db.String(20))
    remark = db.Column(db.String(400))
    store_tag = db.Column(db.String(100))
    search_tag = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    store_img = db.Column(db.String(200))

'''
#flask admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Store, db.session))
'''

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#login
@app.route("/",methods=['GET','POST'])
def login():
    session.permanent = True
    if request.method == 'POST':
    
        password = request.form.get('password')
        
        user1 = User.query.filter_by(authority="管理者").first()
        user2 = User.query.filter_by(authority="一般").first()
        
        if check_password_hash(user1.password, password):
            login_user(user1)
            return render_template('auth/login.html', )
        elif check_password_hash(user2.password, password):
            login_user(user2)
            return render_template('auth/login.html')
        elif password == '':
            err_msg = "パスワードを入力してください"
            return render_template('auth/login.html', err_msg = err_msg)
        else:
            err_msg = "パスワードが違います"
            return render_template('auth/login.html', err_msg = err_msg)
    else:
        return render_template('auth/login.html')
        
#password signup
@app.route("/signup", methods=['GET','POST'])
@login_required
def signup():
    if request.method == 'POST':
        
        authority = request.form.get('authority')
        password = request.form.get('password')
        
        if authority == '':
            err_msg = "権限名を入力してください"
            return render_template('auth/signup.html', err_msg = err_msg)
        elif password == '':
            err_msg = "パスワードを入力してください"
            return render_template('auth/signup.html', err_msg = err_msg)
        else:
            user = User(authority = authority, password = generate_password_hash(password, method='sha256'))
            
            db.session.add(user)
            db.session.commit()
            return render_template('auth/signup.html', authority = authority, password = password)
        
    else:
        return render_template('auth/signup.html')
    
#password edit
@app.route("/edit", methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'POST':
        
        user1 = User.query.filter_by(authority="管理者").first()
        user2 = User.query.filter_by(authority="一般").first()
        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if password1 == "" or password2 == "":
            err_msg = "パスワードを入力してください"
            return render_template('auth/edit.html', err_msg = err_msg)
        elif password1 == password2:
            err_msg = "パスワードが重複しています"
            return render_template('auth/edit.html', err_msg = err_msg)
        else:
            try:
                user1.password = generate_password_hash(password1, method='sha256')
                user2.password = generate_password_hash(password2, method='sha256')
                
                db.session.commit()
                
                return render_template('auth/edit.html', password1 = password1, password2 = password2)
            
            except:
                err_msg = "実行に失敗しました"
                return render_template('auth/except.html', err_msg = err_msg)
    
    else:
        return render_template("auth/edit.html")
    
#logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

#search
@app.route('/search', methods=['GET','POST'])
@login_required
def search():
     
    if request.method == 'POST':
        
        keyword = request.form.get('keyword')
        pref = request.form.get('pref')
        industry = request.form.get('industry')
        keyword_filter = "%{}%".format(keyword)
        pref_filter = "%{}%".format(pref)
        
        if keyword != '' and pref != '' and industry != '':

            err_msg = "検索結果が見つかりませんでした"
            store_all = Store.query.filter(or_(Store.name.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.pref.like(pref_filter), Store.industry == industry).all()
            store_count = Store.query.filter(or_(Store.name.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.pref.like(pref_filter), Store.industry == industry).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword != '' and pref != '' and industry == '':
            
            err_msg = "検索結果が見つかりませんでした"
            store_all = Store.query.filter(or_(Store.name.like(keyword_filter),Store.industry.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.pref == pref).all()
            store_count = Store.query.filter(or_(Store.name.like(keyword_filter),Store.industry.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.pref == pref).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword == '' and pref != '' and industry != '':

            err_msg = "検索結果が見つかりませんでした"
            store_all = Store.query.filter_by(pref = pref, industry = industry).all()
            store_count = Store.query.filter_by(pref = pref, industry = industry).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword != '' and pref == '' and industry != '':

            err_msg = "検索結果が見つかりませんでした"
            store_all = Store.query.filter(or_(Store.name.like(keyword_filter),Store.pref.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.industry == industry).all()
            store_count = Store.query.filter(or_(Store.name.like(keyword_filter),Store.pref.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter)), Store.industry == industry).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword != '' and pref == '' and industry == '':

            err_msg = "キーワードに該当する店舗が見つかりませんでした"
            store_all = Store.query.filter( or_(Store.name.like(keyword_filter),Store.industry.like(keyword_filter),Store.pref.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter))).all()
            store_count = Store.query.filter( or_(Store.name.like(keyword_filter),Store.industry.like(keyword_filter),Store.pref.like(keyword_filter),Store.area.like(keyword_filter),Store.store_area.like(keyword_filter),Store.concept.like(keyword_filter))).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword == '' and pref != '' and industry == '':

            err_msg = "エリアに該当する店舗が見つかりませんでした"
            store_all = Store.query.filter(Store.pref.like(pref_filter)).all()
            store_count = Store.query.filter(Store.pref.like(pref_filter)).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        elif keyword == '' and pref == '' and industry != '':

            err_msg = "業種に該当する店舗が見つかりませんでした"
            store_all = Store.query.filter_by(industry = industry).all()
            store_count = Store.query.filter_by(industry = industry).count()

            return render_template('auth/search.html', err_msg = err_msg, store_all = store_all, count = store_count)

        else:

            store_all = Store.query.all()
            print(store_all)
            store_count = Store.query.count()

            return render_template('auth/search.html', store_all = store_all, count = store_count)
        
    else:
        return render_template('auth/search.html')

#store create
@app.route("/create", methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        
        name = request.form['name']
        industry = request.form['industry']
        rank = request.form['rank']
        beforeP = request.form.getlist('pref')
        pref = ",".join(beforeP)
        area = request.form['area']
        store_area = request.form['store_area']
        station = request.form['station']
        time = request.form['time']
        beforeC = request.form.getlist('concept')
        concept = ",".join(beforeC)
        age = request.form['age']
        salary = request.form['salary']
        nomination = request.form['nomination']
        guarantee = request.form['guarantee']
        face = request.form['face']
        dormitory = request.form['dormitory']
        sundry = request.form['sundry']
        back = request.form['back']
        remark = request.form['remark']
        beforeT = request.form.getlist('store_tag')
        store_tag = ",".join(beforeT)
        search_tag = str(request.form.getlist('store_tag'))
        pic = request.files['pic']
        
        if name != '' and industry != '' and rank != '' and pref != '' and salary != '':

            if not pic:
                img = 'img/storeLink.jpg'
            else:
                filedir = 'static/'
                filename = 'img/' + secure_filename(pic.filename)
                filepath = filedir + filename
                pic.save(filepath)
                img = filename
                
                try:
                    storeList = Store(name = name, industry = industry, rank = rank, pref = pref, area = area, store_area = store_area, station = station, time = time, concept = concept, age = age, salary = salary, nomination = nomination, guarantee = guarantee, face = face, dormitory = dormitory, sundry = sundry, back = back, remark = remark, store_tag = store_tag, search_tag = search_tag, store_img = img)
                        
                    db.session.add(storeList)
                    db.session.commit()
                        
                    return render_template('auth/create.html', store = storeList)
                except:
                    return render_template('auth/except.html')
            
        else:
            
            err_msg = "＊必須項目を入力してください"
            return render_template('auth/create.html', err_msg = err_msg)
            
    else:
        return render_template("auth/create.html")
    
#store update
@app.route("/<int:id>/update", methods=['GET','POST'])
@login_required
def update(id):
    storeList = Store.query.get(id)
    
    if request.method == 'POST':
        
        storeList.name = request.form['name']
        storeList.industry = request.form['industry']
        storeList.rank = request.form['rank']
        beforeP = request.form.getlist('pref')
        storeList.pref = ",".join(beforeP)
        storeList.area = request.form['area']
        storeList.store_area = request.form['store_area']
        storeList.station = request.form['station']
        storeList.time = request.form['time']
        beforeC = request.form.getlist('concept')
        storeList.concept = ",".join(beforeC)
        storeList.age = request.form['age']
        storeList.salary = request.form['salary']
        storeList.nomination = request.form['nomination']
        storeList.guarantee = request.form['guarantee']
        storeList.face = request.form['face']
        storeList.dormitory = request.form['remark']
        storeList.sundry = request.form['sundry']
        storeList.back = request.form['back']
        storeList.remark = request.form['remark']
        beforeT = request.form.getlist('store_tag')
        storeList.store_tag = ",".join(beforeT)
        storeList.search_tag = str(request.form.getlist('store_tag'))

        if storeList.name != '' and storeList.industry != '' and storeList.rank != '' and storeList.pref != '' and storeList.salary != '':

            try:
                db.session.commit()
                        
                return render_template('auth/detail.html', store = storeList)
            except:
                return render_template('auth/except.html')

        else:
                
            err_msg = "＊必須項目を入力してください"

            return render_template('auth/update.html', store = storeList, err_msg = err_msg)
            
    else:
        return render_template('auth/update.html', store = storeList)

#store img
@app.route("/<int:id>/img", methods=['GET','POST'])
@login_required
def img(id):
    storeList = Store.query.get(id)
    if request.method == 'POST':

        pic = request.files['pic']

        if not pic:

            err_msg = "＊画像を指定してください"

            return render_template('auth/img.html', store = storeList, err_msg = err_msg)

        else:

            try:

                filedir = 'static/'
                filename = 'img/' + secure_filename(pic.filename)
                filepath = filedir + filename
                pic.save(filepath)
                img = filename

                storeList.store_img = img

                db.session.commit()

                return render_template('auth/img.html', store = storeList)

            except:
                return render_template('auth/except.html')

    else:
        return render_template('auth/img.html', store = storeList)
    
#store destroy
@app.route("/<int:id>/destroy", methods=['GET'])
@login_required
def destroy(id):
    storeList = Store.query.get(id)
    
    db.session.delete(storeList)
    db.session.commit()
    return redirect(url_for('search'))

#store detail
@app.route("/<int:id>/detail")
@login_required
def detail(id):
    storeList = Store.query.get(id)
    return render_template('auth/detail.html', store = storeList)

@app.route("/favorite", methods=['GET'])
@login_required
def favorite():

    err_msg = "おすすめの店舗が登録されていません"
    store_all = Store.query.filter(Store.store_tag.like("%おすすめ%")).all()
    store_count = Store.query.filter(Store.store_tag.like("%おすすめ%")).count()

    return render_template('auth/favorite.html', err_msg = err_msg, store_all = store_all, count = store_count)

@app.route("/info", methods=['GET'])
@login_required
def info():

    err_msg = "店舗を登録してください"
    store_all = Store.query.order_by(Store.created_at.asc()).limit(5).all()

    return render_template('auth/info.html', err_msg = err_msg, store_all = store_all)