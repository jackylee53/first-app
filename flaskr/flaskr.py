#-*- coding: utf8-*-
#调用database.py链接数据库
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
import sys

#设置输入格式为utf8
reload(sys)
sys.setdefaultencoding('utf8')
#定义flask配置项目为一个python类
class Configs():
    DATABASE = './flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

app = Flask(__name__)
#调用flask配置项目的类
app.config.from_object(Configs)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#before_request装饰器。在请求之前执行什么命令
@app.before_request
def before_request():
    #g只保存一次请求，并且每个函数都可用
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title,text from entries order by id DESC ')
    #fetchall接收所有返回的数据
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST'])
def add_entry(charset='utf-8'):
    #检查是否已经登录。没有登录返回401错误
    if not session.get('logged_in'):
        abort(401)
    #g.db.execute执行一个插入数据库的任务。内容从表单的title和text中来。
    #注意sql语句中的？号用来替代参数，并将参数放到一个列表中传递给sql语句。用来防止sql注入
    g.db.execute('insert into entries (title, text) VALUES (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('新的条目已经插入')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login(charset='utf-8'):
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = '用户名不正确'.decode(charset)
        elif request.form['password'] != app.config['PASSWORD']:
            error = '密码不正确'.decode(charset)
        else:
            #在会话为logged_in的键设置一个True值用于对是否登录成功进行验证
            session['logged_in'] = True
            flash('您登录成功')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout(charset='utf-8'):
    #使用pop方法删除logged_in键的值
    session.pop('logged_in', None)
    flash('您已经退出').decode(charset)
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0'
    )