# -*- coding: utf-8 -*-
from . import parsers as p
from homework_project.config.syntax import syntax


def main_sql():
    while True:
        sql_list = input('请输入sql语句>').strip().split()
        print(sql_list)
        if sql_list:
            sql_type = sql_list[0] # 获取收入sql语句的类型
            if sql_type in syntax('all'):
                p.parses(sql_type)(sql_list, sql_type) # 调用parsers模块的parses函数进行语法解析
            else:
                print('sql语法错误，请使用help命令查看帮助。')
        else:
            continue


