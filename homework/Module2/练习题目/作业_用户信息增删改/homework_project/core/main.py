# -*- coding: utf-8 -*-
from . import parsers as p
from homework_project.config.syntax import syntax
from .actions import actions
import os

def main_sql():
    database_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/database/'
    while True:
        sql_str = input('请输入sql语句>').strip()
        if sql_str:
            sql_type = sql_str.split()[0].lower() # 获取输入的sql语句的类型。
            if sql_type in syntax('all'):  # 先检查一下sql语句的类型是否在syntax函数中定义。如没有定义先请用户查看帮助
                dict_sql = p.parses(sql_type)(sql_str, sql_type, database_dir) # 调用parsers模块的parses函数进行语法解析
                if dict_sql:
                    print(dict_sql)
                    actions(sql_type, dict_sql)(dict_sql)
            else:
                print('sql语法错误，请使用h命令查看帮助。')
        else:
            continue



