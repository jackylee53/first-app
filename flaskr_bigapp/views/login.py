#-*- coding:utf8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask import current_app

from flaskr_bigapp.lib.db.database import Database
from flaskr_bigapp.lib.sys.message import Message

login = Blueprint('login', __name__)
@login.route('/login', methods=['GET', 'POST'])
def login_form():
    error = None
    database = Database() #创建DATABASE类的实例
    message = Message()
    if request.method == 'POST':
       for user in database.query_db('select user,password from users'):
           if  request.form['username'] != user['user']:
               error = message.error_message('USER_E_M')
           elif request.form['password'] != user['password']:
               error = current_app.config['PASS_E_M']
           else:
               session['logged_in'] = True
               flash(current_app.config['LOGIN_M'])
               return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)