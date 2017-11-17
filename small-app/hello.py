from flask import Flask,request,render_template

small = Flask(__name__)
@small.route('/')
def fuck_you():
    return 'Fuck you!'

@small.route('/hello')
def hello_world():
    return 'Hello World!'

@small.route('/user/<username>')
def show_user_profile(username=None):
    return 'User %s' % username

@small.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'POST'
    else:
        return 'GET'

@small.route('/html/')
@small.route('/hello/<name>')
def html(name=None):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    small.debug = True
    small.run(host='0.0.0.0')