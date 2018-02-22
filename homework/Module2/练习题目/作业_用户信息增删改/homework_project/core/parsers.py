# -*- coding: utf-8 -*-
from homework_project.config.syntax import syntax
from homework_project.action.actions import actions
from .check_syntax import check_syntax as check
from .help import help


def parses(sql_list, sql_type):
    dict_sql = syntax(sql_type) #导入初始的sql语法
    for i in sql_list:
        if i in dict_sql:
            key = i
        else:
            dict_sql[key].append(i)
    if 'where' in dict_sql:
        where_parses(sql_type, dict_sql)
    if 'set' in dict_sql:
        set_parses(sql_type, dict_sql)
    if 'values' in dict_sql:
        values_parses(sql_type, dict_sql)
    print(dict_sql)
    actions(sql_type, dict_sql)

def where_parses(sql_type, dict_sql):
    key = ['<', '>', '=', 'like']
    if len(dict_sql['where']) < 3:  # 如果where语句不输入空格，dict_sql['where']值的列表的值的数量会小于3。直接提示帮助。
        print(help(sql_type))
    if dict_sql['where'][1] not in key:
            print('where语句错误，必须包含%s字符'%key)
    else:
        return dict_sql


def set_parses(sql_type, dict_sql):
    key = ['=']
    if len(dict_sql['set']) < 3: # 如果set语句不输入空格，dict_sql['set']值的列表的值的数量会小于3。直接提示帮助。
        print(help(sql_type))
    if dict_sql['set'][1] not in key:
        print('set语句错误，必须包含%s字符'%key)
    else:
        return dict_sql


def values_parses(sql_type, dict_sql):
    if not len(dict_sql['values']):
        print(help(sql_type))
    else:
        dict_sql['values'] = ' '.join(dict_sql['values']).split(',')
        return dict_sql


