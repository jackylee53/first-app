# -*- coding: utf-8 -*-
import re
#from .help import help


def parsers(sql_str, sql_type, base_dir):
    """ 语法解析函数

    :param sql_type: 从main()函数导入的sql语句类型。
    :return:
        parsers_dict[sql_type]
        相应的语法解析函数
    """
    parsers_dict = {'select': select_parser,
                    'add': add_parser,
                    'del': del_parser,
                    'update': update_parser}
    if sql_type in parsers_dict:
        return parsers_dict[sql_type](sql_str, sql_type, base_dir)
    else:
        return False


def select_parser(sql_str, sql_type, base_dir):
    """ 搜索语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
    """
    dict_sql = {}  # 创建空字典
    command_parse = re.search(r'select\s(.*?)\sfrom\s(.*?)\swhere\s(.*)', sql_str, re.I)  # 使用正则表达式解析add语法，并且re.I忽略大小写
    if command_parse:
        dict_sql['select'] = command_parse.group(1)
        dict_sql['from'] = base_dir + command_parse.group(2)  # sql字典'from’键添加数据库表文件路径的值
        dict_sql['where'] = command_parse.group(3)  # sql字典‘where’键添加插入的值
        if logic_cal(dict_sql['where']):  # 使用logic_cal函数将where语句语法再次进行解析
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def add_parser(sql_str, sql_type, base_dir):
    """ 添加语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'add\sto\s(.*?)\svalues\s(.*)', sql_str, re.I)  # 使用正则表达式解析add语法，并且re.I忽略大小写
    if command_parse:
        dict_sql['to'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['values'] = command_parse.group(2).split(',')  # sql字典‘values’键添加插入的值
        return dict_sql
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def del_parser(sql_str, sql_type, base_dir):
    """ 删除语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'del\sfrom\s(.*?)\swhere\s(.*)', sql_str, re.I)
    if command_parse:
        dict_sql['from'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['where'] = command_parse.group(2)  # sql字典‘where’键添加插入的值
        if logic_cal(dict_sql['where']):  # 使用logic_cal函数将where语句语法再次进行解析
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def update_parser(sql_str, sql_type, base_dir):
    """ 更新语句解析函数

    :param sql_str: 用户输入的sql语句
    :param sql_type: 用户输入的sql语句类型
    :param base_dir: 主函数导入的数据库所在路径
    :return:
        dict_sql
        解析后的字典格式sql语句
    """
    dict_sql = {}
    command_parse = re.search(r'update\s(.*?)\sset\s(.*?)=(.*?)\swhere\s(.*)', sql_str, re.I)
    if command_parse:
        dict_sql['update'] = base_dir + command_parse.group(1)  # sql字典'to’键添加数据库表文件路径的值
        dict_sql['set'] = [command_parse.group(2), '=', command_parse.group(3)]  # sql字典‘where’键添加插入的值
        dict_sql['where'] = command_parse.group(4)
        if logic_cal(dict_sql['where']) and logic_cal(dict_sql['set']):  # 如果where语句、set语句都符合logic_cal中定义的规范
            dict_sql['where'] = logic_cal(dict_sql['where'])  # 如解析有返回值，将返回值重新作为dict_sql['where']的值
            dict_sql['set'] = logic_cal(dict_sql['set'])  # 如解析有返回值，将返回值重新作为dict_sql['set']的值
            return dict_sql
        else:
            print(help(sql_type))  # 当语法解析不正常答应帮助
    else:
        print(help(sql_type))  # 当语法解析不正常答应帮助


def logic_cal(logic_exp):
    """ 逻辑函数

    :param logic_exp: sql语句中和逻辑判断相关的语句，列表格式。如[‘age','>=',20] 或 [‘dept','like','HR']
    :return:
        logic_exp
        经过语法解析后的逻辑判断语句。列表格式。如[‘age','==',20] 或 [‘dept','like','HR']
    """
    # 表达式列表优化成三个元素，形如[‘age','>=',20] 或 [‘dept','like','HR']
    logic_exp = re.search('(.+?)\s([=<>]{1,2}|like)\s(.+)', ''.join(logic_exp))
    if logic_exp:
        logic_exp = list(logic_exp. group(1, 2, 3))  # 取得re匹配的所有值，并作为一个列表
        if logic_exp[1] == '=':
            logic_exp[1] = '=='
        # 判断逻辑运算的比较符号后的值是否字母，并且用户是否输入了双引号。如没有输入手工添加上双引号。
        if not logic_exp[2].isdigit() and not re.search('"(.*?)"', logic_exp[2]):
            logic_exp[2] = '"' + logic_exp[2] + '"'
        return logic_exp
    else:
        return False
