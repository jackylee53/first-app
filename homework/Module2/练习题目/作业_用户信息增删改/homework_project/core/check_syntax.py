# -*- coding: utf-8 -*-
import re

def check_syntax(dict_sql):
    ''' sql语句检查函数。

    :param sql_type:
    :param dict_sql:
    :return:
    '''
    tmp_list = []
    for key in dict_sql:
        tmp_list.append(key)  # 将sql语句字典中所有的关键字缓存在一个列表中
        if not dict_sql[key] and dict_sql[key] is not False:
            return 1
        else:
            return dict_sql


def where_c_syntax(dict_sql):
    key = ['<', '>', '=', 'like']
    if len(dict_sql['where']) < 3:  # 如果where语句不输入空格，dict_sql['where']值的列表的值的数量会小于3。直接提示帮助。
        return 1
    elif dict_sql['where'][1] not in key:
        return 1
    elif len(dict_sql['where']) > 3:  # 当where语句列表大于3时，可以判断这个
        if dict_sql['where'][1] in key:
            key,item = ' '.join(dict_sql['where']).split(dict_sql['where'][1])
            dict_sql['where'] = [key.strip().strip('"'),dict_sql['where'][1],item.strip().strip('"')]
            return dict_sql
    else:
        return dict_sql

def set_c_syntax(dict_sql):
    key = ['=']
    if len(dict_sql['set']) < 3: # 如果set语句不输入空格，dict_sql['set']值的列表的值的数量会小于3。直接提示帮助。
        return 1
    elif dict_sql['set'][1] not in key:
        return 1
    elif len(dict_sql['set']) > 3:  # 当where语句列表大于3时，可以判断这个
        if dict_sql['set'][1] in key:
            key,item = ' '.join(dict_sql['set']).split(dict_sql['set'][1])
            dict_sql['set'] = [key.strip().strip('"'),dict_sql['set'][1],item.strip().strip('"')]
            print(key,item)
            return dict_sql
    else:
        return dict_sql


def values_check(dict_sql):
    if not len(dict_sql['values']):
        return 1
    else:
        dict_sql['values'] = ' '.join(dict_sql['values']).split(',')
        return dict_sql