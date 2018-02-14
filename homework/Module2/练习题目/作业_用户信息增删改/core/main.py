# -*- coding: utf-8 -*-
from homework.Module2.练习题目.作业_用户信息增删改.core import parsers
def main_sql():
    sql_list = input('请输入sql语句>').strip().split(' ')
    if sql_list[0] == 'select':
        parsers.select_parses(sql_list)

if __name__ == '__main__':
    main_sql()


