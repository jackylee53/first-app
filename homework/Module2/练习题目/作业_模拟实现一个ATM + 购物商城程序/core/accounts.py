#!_*_coding:utf-8_*_
import json
import time
from core import database
from conf import settings
from core import parsers
from core import actions


def load_accounts(account):
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
    base_dir = settings.DATABASE['path']
    sql_str = 'update accounts_table set %s where account = %s' % (set_str, account)
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    actions.actions(sql_type, dict_sql)


def add_account(*args, **kwargs):
    #print(args)
    base_dir = settings.DATABASE['path']
    sql_str = 'add to accounts_table values %s' % (','.join(args))
    sql_type = sql_str.split()[0]
    dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
    actions.actions(sql_type, dict_sql)
