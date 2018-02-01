#-*- coding: utf8 -*-
USER_E_M = '用户名不正确'
PASS_E_M = '密码不正确'
LOGIN_M = '登录成功'
LOGOUT_M = '退出成功'
INSERT_M = '已添加新内容'
REG_U_E_M = '用户已存在'
REG_P_E_M = '非重复密码'
REG_M = '注册成功'

class Message():
    def __init__(self):
        pass;

    def error_message(self, message):
        self.message = message
        if self.message == 'USER_E_M':
            return USER_E_M