#-*- coding: utf8 -*-
#定义flask配置项目为一个python类
class Config(object):
    USERNAME = 'admin'
    PASSWORD = 'default'
    DATABASE = './flaskr.db'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development key'

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True

class Message():
    USER_E_M = '用户名不正确'
    PASS_E_M = '密码不正确'
    LOGIN_M = '登录成功'
    LOGOUT_M = '退出成功'
    INSERT_M = '已添加新内容'
    REG_U_E_M = '用户已存在'
    REG_P_E_M = '非重复密码'
    REG_M = '注册成功'


