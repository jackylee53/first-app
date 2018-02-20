# -*- coding: utf-8 -*-
from homework_project.config.syntax import syntax
from homework_project.action.actions import actions
from .check_syntax import check_syntax as check



def parses(sql_list, sql_type):
    dict_sql = syntax(sql_type) #导入初始的sql语法
    for i in sql_list:
        print(i)
        if i in dict_sql:
            key = i
        else:
            dict_sql[key].append(i)
    result = check(sql_type, dict_sql)
    if type(result) is dict:
        print(result)
        actions(sql_type, dict_sql)
    else:
        print(check(sql_type, dict_sql))



