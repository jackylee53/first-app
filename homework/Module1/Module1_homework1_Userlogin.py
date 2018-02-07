#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
作业需求：
基础需求：
让用户输入用户名密码
认证成功后显示欢迎信息
输错三次后退出程序
升级需求：
可以支持多个用户登录(提示，通过列表存多个账户信息)
用户3次认证失败后，退出程序，再次启动程序尝试登录时，还是锁定状态（提示:需把用户锁定的状态存到文件里）
'''
import time
class User_Login(object):
    #初始化参数
    def __init__(self):
        self.user_list = ['henry','tom','jenry']
        self.pass_list = ['henry123','tom123','jenry123']
        self.lock_file = '/tmp/lock_file'
    #读取锁定文件函数
    def read_lock(self):
        rf = open(self.lock_file,"r")
        return rf.read()

    #写入锁定文件函数
    def write_lock(self,status):
        wf = open(self.lock_file,"w")
        #通过函数外部变量的导入，来判断登录是否成功与失败。失败就在锁定文件中输入1，成功就在锁定文件中输入0
        if status == 0:
            wf.write('0')
        else:
            wf.write('1')

    def login(self):
        #判断锁定文件的值，如果为1。锁定5秒后恢复再次登录的权限。
        if self.read_lock() == '1':
            print('Your account is locked! Please wait 5 second.')
            time.sleep(5)
            self.write_lock(status=0)
        else:
        #如果锁定文件不为1,。要求用户输入账号和密码
            count = 0
            while count < 3:
                user = input("Please input Username: ").strip()
                if not user: continue
                passw = input("Please input Password: ").strip()
                if not user: continue
                count += 1
                if user in self.user_list:
                    index = self.user_list.index(user)
                    if passw == self.pass_list[index]:
                        self.write_lock(status=0)
                        print('Welcome %s login!'%user)
                        break
                    else:
                        self.write_lock(status=1)
                        print('Password error!')
                        continue
                else:
                    self.write_lock(status=1)
                    print('Username error!')
                    continue

if __name__ == '__main__':
    homework = User_Login()
    homework.login()