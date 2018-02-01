#-*- coding: utf8-*-
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
import sys
'''
第一步：导入sys模块，使用setdefultencoding函数将笨程序中的输出内容都转换为utf8。防止中文输出时出现乱码报错。
'''
reload(sys)
sys.setdefaultencoding('utf8')

'''
第二步：初始化一个flask实例，并且命名为app
'''
app = Flask(__name__, instance_relative_config=True)
'''
第三部.flask获取配置的三种方法：
1.)可以使用config.from_object()调用某个模块对象中的类作为配置项
app.config.from_object('config.TestingConfig')
'''
app.config.from_object('config.Message')
'''

2.)可以使用config.from_pyfile()调用同级目录下instance目录的某个配置文件作为配置项。
如果在定义Flask实例时app = Flask(__name__, instance_path='')，使用instance_path。就会在这个绝对路径中查找配置文件。
如果使用了instance_relative_config=True，则是在同级目录下的instance目录下查找配置文件。
'''
app.config.from_pyfile('application.cfg', silent=True)
'''
3.)可以使用config.from_envvar()调用环境变量中的APPLICATION_CONFIG环境变量。
app.config.from_envvar('APPLICATION_CONFIG')
'''

'''
使用config.from_pyfile('application.cfg', silent=True)定义的application.cfg配置文件中的MODE配置，来判断flask使用哪种类型的配置项目。
'''
if app.config['MODE'] == 'Production':
    app.config.from_object('config.ProductionConfig')
elif app.config['MODE'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif app.config['MODE'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.logger.error('Application mode non-existent!')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

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
    #fetchall接收所有返回的数据.可以通过fetchall获得多行数据。但返回结果是元组。通过使用dict（）函数将元组数据转换成字典。并赋予一个entries的列表中
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
    flash(app.config['INSERT_M'])
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login(charset='utf-8'):
    error = None
    if request.method == 'POST':
#使用配置文件检查用户名和密码是否正确
#        if request.form['username'] != app.config['USERNAME']:
#            error = app.config['USER_E_M']
#        elif request.form['password'] != app.config['PASSWORD']:
#            error = app.config['PASS_E_M']
#        else:
       #使用sqlite3的user数据库检查用户是否可以登录
       for user in query_db('select user,password from users'):
           if  request.form['username'] != user['user']:
               error = app.config['USER_E_M']
           elif request.form['password'] != user['password']:
               error = app.config['PASS_E_M']
           else:
               session['logged_in'] = True
               flash(app.config['LOGIN_M'])
               return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        for user in query_db('select user,password from users'):
            if request.form['username'] == user['user']:
                error = app.config['REG_U_E_M']
            elif request.form['password'] != request.form['confirm_password']:
                error = app.config['REG_P_E_M']
            else:
                g.db.execute('insert into users (user, password) VALUES (?, ?)',
                         [request.form['username'], request.form['password']])
                g.db.commit()
                session['logged_in'] = True
                flash(app.config['REG_M'])
                return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)
@app.route('/logout')
def logout(charset='utf-8'):
    #使用pop方法删除logged_in键的值
    session.pop('logged_in', None)
    flash(app.config['LOGOUT_M'])
    '''
    输入日志。但由于没有指定try..except所以没有故障也会输出
    '''
    app.logger.info('fuckyou')
    app.logger.warning('test')
    app.logger.debug('haha')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0'
    )
    '''
    记录日志，并指定日志的格式
    '''
    import logging
    from logging import FileHandler, Formatter
    file_handler = FileHandler('./error.log', mode='a', encoding='UTF-8')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s' '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)