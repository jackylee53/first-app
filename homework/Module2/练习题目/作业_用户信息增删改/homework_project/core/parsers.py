# -*- coding: utf-8 -*-
from homework_project.config.syntax import syntax
from homework_project.action.actions import actions
from .check_syntax import where_c_syntax, check_syntax, values_check
from .help import help


def parses(sql_type):
    """ 语法解析函数

    :param sql_list: 从main()函数导入的用户输入的sql语句列表。
    :param sql_type: 从main()函数导入的sql语句类型。
    :return:
    """
    parsers_dict = {'select': select_parser,
                    'add': add_parser,
                    'del': del_parser,
                    'update': update_parser}
    if sql_type in parsers_dict:
        return parsers_dict[sql_type]


def select_parser(sql_list, sql_type):
    """ select语法解析函数

    :param sql_list:
    :param sql_type:
    :return:
    """
    dict_sql = syntax(sql_type)  # 从config包、syntax模块、syntax函数中导入默认的sql语法。
    if 'where' not in sql_list:  # 如果用户没有输入where语句。
        dict_sql.pop('where')
    else:
        key = ''
        for i in sql_list:  # 用户输入的sql与默认的sql语法进行合并。并形成字典格式的sql语句。进行程序内部的传递。
            if i in dict_sql:
                key = i
            else:
                dict_sql[key].append(i)
    if [] in dict_sql.values():  # 判断sql字段中的key的值是否有空的列表。如果有就表明，用户没有输入的语法不正确
        print(help(sql_type))
    else:
        print(where_parser(dict_sql['where']))
        if where_parser(dict_sql['where']) == 1:
            print(help(sql_type))
        else:
            dict_sql['where'] = where_parser(dict_sql['where'])
            actions(sql_type, dict_sql)


def add_parser(sql_list, sql_type):
    key = ''
    dict_sql = syntax(sql_type)  # 从config包、syntax模块、syntax函数中导入默认的sql语法。
    for i in sql_list:  # 用户输入的sql与默认的sql语法进行合并。并形成字典格式的sql语句。进行程序内部的传递。
        if i in dict_sql:
            key = i
        else:
            dict_sql[key].append(i)
    if [] in dict_sql.values():  # 判断sql字段中的key的值是否有空的列表。如果有就表明，用户没有输入的语法不正确
        print(help(sql_type))
    else:
        dict_sql['values'] = ' '.join(dict_sql['values']).split(',')  # 对values的进行一次重构。主要用于"Alex Li"这种带空格的值
        actions(sql_type, dict_sql)


def del_parser(sql_list, sql_type):
    key = ''
    dict_sql = syntax(sql_type)  # 从config包、syntax模块、syntax函数中导入默认的sql语法。
    for i in sql_list:  # 用户输入的sql与默认的sql语法进行合并。并形成字典格式的sql语句。进行程序内部的传递。
        if i in dict_sql:
            key = i
        else:
            dict_sql[key].append(i)
    if [] in dict_sql.values():  # 判断sql字段中的key的值是否有空的列表。如果有就表明，用户没有输入的语法不正确
        print(help(sql_type))
    else:
        print(where_parser(dict_sql['where']))
        if where_parser(dict_sql['where']) == 1:
            print(help(sql_type))
        else:
            dict_sql['where'] = where_parser(dict_sql['where'])
            actions(sql_type, dict_sql)


def update_parser():
    pass


def where_parser(where_list):
    key = ['<', '>', '=', 'like']
    if len(where_list) < 3:  # 如果where语句不输入空格，dict_sql['where']值的列表的值的数量会小于3。直接提示帮助。
        return 1
    elif where_list[1] not in key:
        return 1
    elif len(where_list) > 3:  # 当where语句列表大于3时，可以判断这个
        if where_list[1] in key:
            key,item = ' '.join(where_list).split(where_list[1])
            where_list = [key.strip().strip('"'),where_list[1],item.strip().strip('"')]
            return where_list
    else:
        temp_list = []
        for i in where_list:
            temp_list.append(i.strip('"'))
        return temp_list
