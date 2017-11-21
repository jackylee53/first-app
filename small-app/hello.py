#-*- coding:utf-8 –*-
from flask import Flask,request,render_template,redirect,url_for,abort,make_response


small = Flask(__name__)
#flask的路由
@small.route('/')
def fuck_you():
    return 'Index Page'

@small.route('/hello')
def hello_world():
    return 'Hello World!'

#flask的变量定义规则
@small.route('/user/<username>')
def show_user_profile(username=None):
    return 'User %s' % username

@small.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@small.route('/post-float/<float:post_float_id>')
def show_post(post_float_id):
    return 'Post Float %d' % post_float_id

#判断http方法，当使用不同的方法时执行不同的语句
@small.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'POST'
    else:
        return 'GET'

#渲染模板
@small.route('/template/')
@small.route('/template/<name>')
def html(name=None):
    return render_template('index.html', name=name)

#重定向到err路由
@small.route('/redirect')
def red():
    return redirect(url_for('err'))

#返回错误页面
@small.route('/error')
def error():
    abort(401)
    #下面的语句不将执行，直接返回401错误
    return 'haha'

#为错误指定一个自己创建的错误页面，并在head添加数据
@small.errorhandler(401)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'),401)
    resp.headers['X-something'] = 'Fuck'
    return resp

if __name__ == '__main__':
    small.debug = True
    small.run(host='0.0.0.0')