# -*- coding: utf-8 -*-
from . import parsers as p
from .actions import actions
import os


def run():
    """ 主函数
        获取用户输入，并对用户进行解析。如果获取解析值，并执行相应的sql操作。
    """
    database_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/database/'  # 获取数据库文件的路径
    while True:
        sql_str = input('请输入sql语句>').strip()
        if sql_str:
            sql_type = sql_str.split()[0].lower()  # 获取输入的sql语句的类型。
            if p.parses(sql_type):  # 检查sql的类型是否符合规则
                dict_sql = p.parses(sql_type)(sql_str, sql_type, database_dir)  # 调用parsers模块的parses函数进行语法解析
                if dict_sql:  # 如果字典格式的sql语句返回
                    print(actions(sql_type)(dict_sql))  # 则执行后面的sql操作
            else:
                print('sql语法错误，程序支持select，del，add，update语句。')
        else:
            continue
