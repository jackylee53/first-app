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
