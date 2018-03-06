## **功能描述**
作业需求：
```text
1、额度 15000或自定义
2、实现购物商城，买东西加入购物车，调用信用卡接口结账
3、可以提现，手续费5%
4、支持多账户登录
5、支持账户间转账
6、记录每月日常消费流水
7、提供还款接口
8、ATM记录操作日志
9、提供管理接口，包括添加账户、用户额度，冻结账户等。。。
10、用户认证用装饰器
```

注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码！

## **流程图**
程序流程图（待补全）
![]()

## **程序目录结构**
````text
bin
├── atm.py  # atm入口
├── __init__.py
└── manage.py  # 管理入口
conf
├── __init__.py
└── settings.py  # 配置文件
core
├── accounts.py  # 账号添加、修改额度、禁用、启动接口
├── actions.py   # sql动作接口
├── auth.py      # 用户认证接口
├── database.py  # 数据库操作接口
├── db_handler.py# 无用到
├── __init__.py
├── logger.py    # 日志接口
├── main.py      # 主接口
├── parsers.py   # sql语法解析接口
└── transaction.py # 交易接口
db
├── accounts_table  # 用户账号表
└── managers_table  # 管理员账号表
log
├── access.log      #访问日志
└── transactions.log #交易日志

````

## **程序主体**
atm.py
```python
#!_*_coding:utf-8_*_

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.run('atm')

```
manage.py
```python
#!_*_coding:utf-8_*_

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.run('manage')

```
setting.py
```python
#!_*_coding:utf-8_*_
#__author__:"Alex Li"
import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database title summary
TITLE = ['id','name','age','phone','dept','enroll_date','expire_date','account','password','credit','balance','status','pay_day']

# Account database setting
DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name':'accounts_table',
    'path': "%s/db/" % BASE_DIR
}

# Manager account database setting
MANAGE_DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name':'managers_table',
    'path': "%s/db/" % BASE_DIR
}

# logger setting
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

# Transaction setting
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},

}

ACCOUNT_DEFAULT = {
    'credit': 15000.0

}
```
accounts.py
```python
#!_*_coding:utf-8_*_
import json
import time
from core import database
from conf import settings
from core import parsers
from core import actions


def load_accounts(account):
    """ Check account whether exists in a database

    :param account:
    :return:
    """
    base_dir = settings.DATABASE['path']
    sql_str = 'select * from accounts_table where account = %s' % account
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    res = actions.actions(sql_type, dict_sql)
    if not res:
        return False
    else:
        return True


def change_account(account, set_str):
    """ Change account data

    :param account:
    :param set_str:
    :return:
    """
    base_dir = settings.DATABASE['path']
    sql_str = 'update accounts_table set %s where account = %s' % (set_str, account)
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    actions.actions(sql_type, dict_sql)


def add_account(*args):
    """ Add an new account

    :param args:
    :param kwargs:
    :return:
    """
    base_dir = settings.DATABASE['path']
    sql_str = 'add to accounts_table values %s' % (','.join(args))
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    actions.actions(sql_type, dict_sql)

```
actions.py
```python
# -*- coding: utf-8 -*-
from core import database
from conf import settings
import re


def actions(sql_type,dict_sql):
    """ sql操作主函数

    :param sql_type: sql语句的类型
    :return:
        actions_dict[sql_type]
        相应操作的函数
    """
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action}
    if sql_type in actions_dict:  # 判断导入的sql类型是否在actions_dict字典中定义。
        return actions_dict[sql_type](dict_sql)
    else:
        return False


def select_action(dict_sql):
    temp_list = []
    info = dict_sql['select']
    data = database.read_db(dict_sql['from'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    count = 0
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        print(where_action(dict_sql['where']))
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            count += 1
            temp_list.append(values)
    return temp_list


def add_action(dict_sql):
    """ 插入动作
        获取用户输入的values，并在表中插入

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    data = database.read_db(dict_sql['to'])  # 获取原始数据库文件中的所有数据
    value = dict_sql['values']  # 从dict_sql中获取values的列表
    t_id = str(int(data[-1]['id']) + 1)  # 获取原始数据库文件中id列最后一行的id数值，并每次自动+1。然后转换为字符串格式
    value.insert(0, t_id)  # 将添加的id插入到value变量中
    if len(value) != len(settings.TITLE):  # 判断输入值得长度是否等于数据库文件中定义的列的长度
        print('列数不正确')
    else:
        data.append(dict(zip(settings.TITLE, value)))  # 在获取的原始数据中插入行的数据
        database.write_db(dict_sql['to'], data)


def del_action(dict_sql):
    """ 删除动作函数

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    temp_list = []
    data = database.read_db(dict_sql['from'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            temp_list.append(values)  # 如果符合条件，就从data中移除对应的values
    return temp_list
    # print('已删除%s条记录' % len(temp_list))
    # for i in temp_list:
    #     data.remove(i)
    # write_db(dict_sql['from'], data)  # 将新生成的data重新写入文件


def update_action(dict_sql):
    """ 更新动作函数

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    data = database.read_db(dict_sql['update'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    set_key = dict_sql['set'][0]  # 获取set语句中用户输入的key
    set_value = dict_sql['set'][2].strip("'").strip('"')  # 获取set语句中用户输入的value
    count = 0
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            count += 1
            values[set_key] = set_value  # 如果符合条件，使用将set_key的值修改为set_value
    print(data)
    print('已更新%s条记录' % count)
    database.write_db(dict_sql['update'], data)  # 将新生成的data重新写入文件


def where_action(condition):
    """ where语句操作函数

    :param condition: 判断语句。就是字典中where的值
    :return:
    """
    if 'like' in condition:  # 如果like在语句中
        # 将where语句中的第二个参数和，第一个参数进行正则比较。如果执行正常就返回True
        return re.search(condition[2].strip("'").strip('"'), condition[0]) and True

    else:
        return eval(' '.join(condition))  # 除此使用eval进行python的逻辑判断

```
auth.py
````python
#!_*_coding:utf-8_*_
import os
from core import parsers
from core import actions
from core import db_handler
from conf import settings
from core import logger
import json
import time


def login_required(func):
    "验证用户是否登录"

    def wrapper(*args, **kwargs):
        print(args, kwargs)
        # print('--wrapper--->',args,kwargs)
        if args[0].get('is_authenticated'):
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")
    return wrapper


def acc_auth(account, password, type):
    '''
    优化版认证接口
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , retun the account object, otherwise ,return None

    '''
    # table = None
    # base_dir = None
    if type == 'atm':
        base_dir = settings.DATABASE['path']
        table = settings.DATABASE['name']
    elif type == 'manage':
        base_dir = settings.MANAGE_DATABASE['path']
        table = settings.MANAGE_DATABASE['name']
    sql_str = 'select * from %s where account = %s' % (table, account)
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    print(dict_sql)
    res = actions.actions(sql_type, dict_sql)
    print(res)
    if not res:
        print("\033[31;1mAccount ID and password is incorrect!\033[0m")
    elif res[0]['password'] == password:
        print('haha')
        exp_time_stamp = time.mktime(time.strptime(res[0]['expire_date'], "%Y-%m-%d"))
        if time.time() > exp_time_stamp:
            print("\033[31;1mAccount [%s] has expired,please contact the back to get a new card!\033[0m" % account)
        elif res[0]['status'] == 1:
            print("\033[31;1mAccount [%s] has expired,please contact the back to get a new card!\033[0m" % account)
        else:  # passed the authentication
            return res[0]
    else:
        print("\033[31;1mAccount ID and password is incorrect!\033[0m")


def acc_login(user_data, log_obj, type):
    '''
    account login func
    :user_data: user info data , only saves in memory
    :return:
    '''
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 3 :
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        auth = acc_auth(account, password, type)
        if auth:  # not None means passed the authentication
            log_obj.info("account [%s] login system" % account)
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            return auth
        retry_count +=1
    else:
        log_obj.error("account [%s] too many login attempts" % account)
        exit()


def acc_logout(user_data, log_obj):
    account = user_data['account_data']['name']
    user_data['is_authenticated'] = False
    log_obj.info("account [%s] logout system" % account)
    exit("account [%s] logout system" % account)

````
databaase.py
```python
# -*- coding: utf-8 -*-
from conf import settings

def read_db(table):
    """ 读取表文件函数。

    :param table: 表文件参数
    :return: 返回一个包含表文件内容的字典
    """
    title = settings.TITLE
    try:
        main_list = []
        with open(table, 'r', encoding='utf-8') as rf:
            for line in rf:
                temp_list = []
                if line.rstrip('\n').split(',') == title:
                    continue
                else:
                    for values in line.strip('\n').split(','):
                        if values.isdigit():
                            temp_list.append(int(values))
                        else:
                            temp_list.append(values)
                    main_list.append(dict(zip(title, temp_list)))
        return main_list
    except FileNotFoundError as e:
        print(e)
        exit(1)


def write_db(table, data):
    """ 写入表文件函数。

    :param table: 表文件参数
    :param data: 导入的数据。为字典格式
    """
    value2 = ','.join(settings.TITLE) + '\n'
    for values in data:
        temp_list = []
        for value in values.values():
            temp_list.append(str(value))
        value2 += ','.join(temp_list) + '\n'
    with open(file=table, mode='w', encoding='utf-8') as wf:
        wf.write(value2)


def print_info(info, **kwargs):
    """ 打印函数。
        用于select语句打印显示

    :param info: select语句中需要显示的类
    :param kwargs: 字典，用于进行操作的原始数据
    :return:
    """
    temp_list = []
    if info == '*':
        for key in kwargs:
            temp_list.append(str(kwargs[key]))
        print(','.join(temp_list))
    else:
        info_list = info.split(',')
        for i in info_list:
            temp_list.append(str(kwargs[i]))
        print(','.join(temp_list))

```
logger.py
```python
#!_*_coding:utf-8_*_
"""
handle all the logging works
"""

import logging
from conf import settings
import time
import re

def logger(log_type):

    # create logger
    my_logger = logging.getLogger(log_type)
    my_logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    my_logger.addHandler(ch)
    my_logger.addHandler(fh)
    return my_logger


def get_log_info(account):
    """ 将日志的内容进行转换后返回相应账号的转款信息

    :param account: 账号参数
    :return:
    """
    temp_list = []
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES['transaction'])
    with open(log_file, 'r') as f:
        for i in f:
            log_mat = re.search('(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}).*account:(.*?)\s.*action:(.*?)\s.*amount:(.*?)\s.*interest:(.*)',i)
            datetime = time.strptime(log_mat.group(1),'%Y-%m-%d %H:%M:%S')
            account_id = log_mat.group(2)
            action = log_mat.group(3)
            amount = log_mat.group(4)
            interest = log_mat.group(5)
            if account_id == account:
                temp_list.append([datetime,action,amount,interest])
    return temp_list
```
main.py
```python
#!_*_coding:utf-8_*_
""""
main program handle module , handle all the user interaction stuff

"""

from core import auth
from core import logger
from core import parsers
from core import transaction
from core.auth import login_required
from core import actions
from conf import settings
from core import accounts
import random
import datetime
import re
import time

# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')


# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}


@login_required
def account_info(acc_data):
    """ print account Information

    :param acc_data: account summary
    :return:
    """
    back_flag = False
    info_temp_list = []
    account_data = acc_data['account_data']
    info_list = ['name', 'age', 'phone', 'enroll_date', 'expire_date', 'account', 'credit', 'balance']
    for i in info_list:
        info_temp_list.append(str(account_data[i]))
    info = ''' --------- BALANCE INFO --------
        username :    {0}
        age:          {1}
        phone:        {2}
        enroll date:  {3}
        expire date:  {4}
        card number:  {5}
        credit:       {6}
        balance:      {7}
        '''.format(*info_temp_list)
    print(info)
    while not back_flag:
        input_b = input("\033[33;1mInput 'b' return to menu:\033[0m").strip()
        if input_b == 'b':
            back_flag = True


@login_required
def repay(acc_data):
    """
    print current balance and let user repay the bill
    :return:
    """
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s'''.format(account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)


@login_required
def withdraw(acc_data):
    """
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    """
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif withdraw_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)


@login_required
def transfer(acc_data):
    """ transfer accounts

    :param acc_data:
    :return:
    """
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        payee_account = input("\033[33;1mInput payee account:\033[0m").strip()
        if payee_account == 'b':
            back_flag = True
        else:
            base_dir = settings.DATABASE['path']
            sql_str = 'select * from accounts_table where account = %s' % payee_account
            sql_type = sql_str.split()[0]
            dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
            res = actions.actions(sql_type, dict_sql)
            if not res:
                print("\033[31;1mThe payee you entered is not a bank user!\033[0m")
            else:
                payee_account_data = res[0]
                trans_amount = input("\033[33;1mInput transfer amount:\033[0m").strip()
                if len(trans_amount) > 0 and trans_amount.isdigit():
                    new_balance = transaction.make_transaction(trans_logger, account_data, 'transfer', trans_amount)
                    payee_balance = transaction.make_transaction(trans_logger, payee_account_data,
                                                                 'repay', trans_amount)
                    if new_balance:
                        print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
                    if payee_balance:
                        print('''\033[42;1mThe money has come to the payee [%s]\033[0m''' % payee_account)
                elif trans_amount == 'b':
                    back_flag = True
                else:
                    print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % trans_amount)


@login_required
def pay_check(acc_data):
    """ Account pay check interface

    :param acc_data:
    :return:
    """
    back_flag = False
    account_id = acc_data['account_id']
    local_month = time.localtime().tm_mon
    res = logger.get_log_info(account_id)

    if res:
        for result in res:
            if result[0].tm_mon == local_month:
                pay_check_info = ''' --------- Datatime %s --------
                Action:       %s
                Amount:       %s
                Interest:     %s''' % (time.strftime('%Y-%m-%d %H:%M:%S',result[0]), result[1], result[2], result[3])
                print(pay_check_info)
    while not back_flag:
        input_b = input("\033[33;1mInput 'b' return to menu:\033[0m").strip()
        if input_b == 'b':
            back_flag = True


@login_required
def logout(acc_data):
    auth.acc_logout(acc_data, access_logger)


def interactive(acc_data):
    """ Atm interactive main interface

    :param acc_data: account summary
    :return:
    """
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  账户信息(功能已实现)
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账(功能已实现)
    5.  账单(功能已实现)
    6.  退出(功能已实现)
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


@login_required
def add_account(acc_data):
    exit_flag = False
    # id, name, age, phone, dept, enroll_date, expire_date, account, password, credit, balance, status, pay_day
    while not exit_flag:
        account_name = input("\033[33;1mInput user name:\033[0m").strip()
        if len(account_name) > 0:
            account_name = account_name
        else:
            continue
        account_age = input("\033[33;1mInput user age:\033[0m").strip()
        if len(account_name) > 0 and account_age.isdigit():
            account_age = account_age
        else:
            continue
        account_phone = input("\033[33;1mInput user phone number:\033[0m").strip()
        if len(account_phone) > 0 and account_phone.isdigit() and len(account_phone) == 11:
            account_phone = account_phone
        else:
            continue
        account_dept = input("\033[33;1mInput user dept:\033[0m").strip()
        if len(account_dept) > 0:
            account_dept = account_dept
        else:
            continue
        account = ''.join(str(random.choice(range(10))) for _ in range(5))  # 随机生成5位账号
        password = input("\033[33;1mInput account password:\033[0m").strip()
        if len(password) == 0:
            password = 'abcde'
        else:
            password = password
        account_enroll_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前时间为开通时间
        account_expire_date = (datetime.datetime.now() + datetime.timedelta(days=(3 * 365))).strftime("%Y-%m-%d")  # 3年后为过期时间
        #print(account_enroll_date,account_expire_date)
        account_credit = input("\033[33;1mInput account credit:\033[0m").strip()
        if len(account_credit) == 0:
            account_credit = str(settings.ACCOUNT_DEFAULT['credit'])
        else:
            account_credit = account_credit


        #print(account)
        input_list = [account_name, account_age,account_phone,account_dept,account_enroll_date,account_expire_date,account,password,account_credit,account_credit,'0','22']
        print(input_list)
        commit = input("\033[33;1mCommit account or exit:(Y/N)\033[0m").strip().upper()
        if commit == 'Y':
            accounts.add_account(*input_list)
            exit_flag = True
        else:
            exit_flag = True


@login_required
def change_credit(acc_data):
    """ Change account credit amount

    :param acc_data:
    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                new_credits = input("\033[33;1mInput new credits amount:\033[0m").strip()
                if len(new_credits) > 0 and new_credits.isdigit():
                    accounts.change_account(dis_account, 'credit = %s' % new_credits)
                else:
                    print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % new_credits)
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")



@login_required
def disable_account(acc_data):
    """ Disable account

    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                accounts.change_account(dis_account, 'status = 1')
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")


@login_required
def enable_account(acc_data):
    """ Enable account

    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                accounts.change_account(dis_account, 'status = 0')
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")



def mg_interactive(acc_data):
    """ Mange interactive main interface

    :param acc_data: 返回的用户账号的具体信息
    :return:
    """
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  添加账号(功能已实现)
    2.  修改额度(功能已实现)
    3.  禁用账号(功能已实现)
    4.  启用账号(功能已实现)
    5.  退出(功能已实现)
    \033[0m'''
    menu_dic = {
        '1': add_account,
        '2': change_credit,
        '3': disable_account,
        '4': enable_account,
        '5': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")

def run(type):
    """
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    if type == 'atm':
        acc_data = auth.acc_login(user_data, access_logger, 'atm')
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            interactive(user_data)
    elif type == 'manage':
        acc_data = auth.acc_login(user_data, access_logger, 'manage')
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            mg_interactive(user_data)

```
parsers.py
```python
# -*- coding: utf-8 -*-
import re
#from .help import help


def parsers(sql_str, sql_type, base_dir):
    """ 语法解析函数

    :param sql_type: 从main()函数导入的sql语句类型。
    :return:
        parsers_dict[sql_type]
        相应的语法解析函数
    """
    parsers_dict = {'select': select_parser,
                    'add': add_parser,
                    'del': del_parser,
                    'update': update_parser}
    if sql_type in parsers_dict:
        return parsers_dict[sql_type](sql_str, sql_type, base_dir)
    else:
        return False


def select_parser(sql_str, sql_type, base_dir):
    """ 搜索语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
    """
    dict_sql = {}  # 创建空字典
    command_parse = re.search(r'select\s(.*?)\sfrom\s(.*?)\swhere\s(.*)', sql_str, re.I)  # 使用正则表达式解析add语法，并且re.I忽略大小写
    if command_parse:
        dict_sql['select'] = command_parse.group(1)
        dict_sql['from'] = base_dir + command_parse.group(2)  # sql字典'from’键添加数据库表文件路径的值
        dict_sql['where'] = command_parse.group(3)  # sql字典‘where’键添加插入的值
        if logic_cal(dict_sql['where']):  # 使用logic_cal函数将where语句语法再次进行解析
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def add_parser(sql_str, sql_type, base_dir):
    """ 添加语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'add\sto\s(.*?)\svalues\s(.*)', sql_str, re.I)  # 使用正则表达式解析add语法，并且re.I忽略大小写
    if command_parse:
        dict_sql['to'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['values'] = command_parse.group(2).split(',')  # sql字典‘values’键添加插入的值
        return dict_sql
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def del_parser(sql_str, sql_type, base_dir):
    """ 删除语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'del\sfrom\s(.*?)\swhere\s(.*)', sql_str, re.I)
    if command_parse:
        dict_sql['from'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['where'] = command_parse.group(2)  # sql字典‘where’键添加插入的值
        if logic_cal(dict_sql['where']):  # 使用logic_cal函数将where语句语法再次进行解析
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def update_parser(sql_str, sql_type, base_dir):
    """ 更新语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'update\s(.*?)\sset\s(.*?)=(.*?)\swhere\s(.*)', sql_str, re.I)
    if command_parse:
        dict_sql['update'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['set'] = [command_parse.group(2), '=', command_parse.group(3)]  # sql字典‘where’键添加插入的值
        dict_sql['where'] = command_parse.group(4)
        if logic_cal(dict_sql['where']) and logic_cal(dict_sql['set']):  # 如果where语句、set语句都符合logic_cal中定义的规范
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            dict_sql['set'] = logic_cal(dict_sql['set'])  # 如解析有返回值，将返回值重新作为dict_sql['set']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def logic_cal(logic_exp):
    """ 逻辑函数

    :param logic_exp: sql语句中和逻辑判断相关的语句，列表格式。如[‘age','>=',20] 或 [‘dept','like','HR']
    :return:
        logic_exp
        经过语法解析后的逻辑判断语句。列表格式。如[‘age','==',20] 或 [‘dept','like','HR']
    """
    # 表达式列表优化成三个元素，形如[‘age','>=',20] 或 [‘dept','like','HR']
    logic_exp = re.search('(.+?)\s([=<>]{1,2}|like)\s(.+)', ''.join(logic_exp))
    if logic_exp:
        logic_exp = list(logic_exp. group(1, 2, 3))  # 取得re匹配的所有值，并作为一个列表
        if logic_exp[1] == '=':
            logic_exp[1] = '=='
        # 判断逻辑运算的比较符号后的值是否字母，并且用户是否输入了双引号。如没有输入手工添加上双引号。
        if not logic_exp[2].isdigit() and not re.search('"(.*?)"', logic_exp[2]):
            logic_exp[2] = '"' + logic_exp[2] + '"'
        return logic_exp
    else:
        return False

```
transaction.py
```python
#!_*_coding:utf-8_*_
from conf import settings
from core import accounts
from core import logger
from core import parsers
from core import actions
#transaction logger


def make_transaction(log_obj, account_data, tran_type, amount, **others):
    '''
    deal all the user transactions
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param others: mainly for logging usage
    :return:
    '''
    amount = float(amount)

    if tran_type in settings.TRANSACTION_TYPE:

        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = float(account_data['balance'])
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest
            #check credit
            if  new_balance <0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is \
                [%s]''' %(account_data['credit'],(amount + interest), old_balance ))
                return
        account_data['balance'] = new_balance
        base_dir = settings.DATABASE['path']
        sql_str = 'update accounts_table set balance = %s where account = %s' % (new_balance, account_data['account'])
        sql_type = sql_str.split()[0]
        dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
        actions.actions(sql_type, dict_sql)
        # accounts.dump_account(account_data)  # save the new balance back to file
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                          (account_data['account'], tran_type, amount,interest) )
        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)

```
## **启动命令**
启动命令。
```text
python atm.py
python manage.py
```

## **发布信息**
    - 作者：henryyuan
    - 日期：2018/03/05
    - 版本：Version 1.0
    - 工具：PyCharm 2017.3.3
    - 版本：Python 3.6.4
    - MarkDown工具：pycharm
    - 流程图工具：ProcessOn
    
## **新闻**
    无

## **历史记录**
    2018-3-5 Version：1.0
    
## **遇到的问题：**
```text
1.) 在main.py接口中的add_account()函数。用于添加账号。需要输入多个input条件。代码如下：
```
```python
account_name = input("\033[33;1mInput user name:\033[0m").strip()
# 有点重复代码的感觉
if len(account_name) > 0:    
    account_name = account_name
else:
    continue
account_age = input("\033[33;1mInput user age:\033[0m").strip()
# 有点重复代码的感觉
if len(account_name) > 0 and account_age.isdigit():
    account_age = account_age
else:
    continue
account_phone = input("\033[33;1mInput user phone number:\033[0m").strip()
# 有点重复代码的感觉
if len(account_phone) > 0 and account_phone.isdigit() and len(account_phone) == 11:
    account_phone = account_phone
else:
    continue
```
```text
每个input语句都需要有if的判断，但当有多个input输入语句时，就会出现过多的重复的if代码。如何减少if语句的代码量。
```