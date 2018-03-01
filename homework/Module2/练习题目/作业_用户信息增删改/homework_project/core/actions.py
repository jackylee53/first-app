# -*- coding: utf-8 -*-
from homework_project.action.database import read_db, write_db, print_info
from homework_project.config.syntax import get_title
import re


def actions(sql_type):
    """ sql操作主函数

    :param sql_type: sql语句的类型
    :return:
        actions_dict[sql_type]
        相应操作的函数
    """
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action}
    if sql_type in actions_dict:  # 判断导入的sql类型是否在actions_dict字典中定义。
        return actions_dict[sql_type]


def select_action(dict_sql):
    temp_list = []
    info = dict_sql['select']
    data = read_db(dict_sql['from'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            print_info(info, **values)


def add_action(dict_sql):
    """ 插入动作
        获取用户输入的values，并在表中插入

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    data = read_db(dict_sql['to'])  # 获取原始数据库文件中的所有数据
    value = dict_sql['values']  # 从dict_sql中获取values的列表
    t_id = str(int(data[-1]['id']) + 1)  # 获取原始数据库文件中id列最后一行的id数值，并每次自动+1。然后转换为字符串格式
    value.insert(0, t_id)  # 将添加的id插入到value变量中
    if len(value) != len(get_title()):  # 判断输入值得长度是否等于数据库文件中定义的列的长度
        print('列数不正确')
    else:
        data.append(dict(zip(get_title(), value)))  # 在获取的原始数据中插入行的数据
        write_db(dict_sql['to'], data)  # 写入文件


def del_action(dict_sql):
    """ 删除动作函数

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    temp_list = []
    data = read_db(dict_sql['from'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            temp_list.append(values)  # 如果符合条件，就从data中移除对应的values
    for i in temp_list:
        data.remove(i)
    write_db(dict_sql['from'], data)  # 将新生成的data重新写入文件


def update_action(dict_sql):
    """ 更新动作函数

    :param dict_sql: parsers函数处理后的字典格式的sql语句
    """
    data = read_db(dict_sql['update'])  # 获取原始数据库文件中的所有数据，data为列表格式
    key = dict_sql['where'][0]  # 获取sql语句中where语句的key值。如id = 1，获取id
    set_key = dict_sql['set'][0]  # 获取set语句中用户输入的key
    set_value = dict_sql['set'][2].strip("'").strip('"')  # 获取set语句中用户输入的value
    for values in data:  # 读取data列表中的每一个元素，values是字典格式
        if type(values[key]) is int:
            value = str(values[key])
        else:
            value = '"' + str(values[key]) + '"'
        dict_sql['where'][0] = value  # 将values[key]的值取出并重新赋值为sql语句的key值。
        if where_action(dict_sql['where']):  # 将新的where语句，发送给where_action语句进行bool判断。
            values[set_key] = set_value  # 如果符合条件，使用将set_key的值修改为set_value
    write_db(dict_sql['update'], data)  # 将新生成的data重新写入文件


def where_action(condition):
    """ where语句操作函数

    :param condition: 判断语句。就是字典中where的值
    :return:
    """
    if 'like' in condition:  # 如果like在语句中
        return re.search(condition[2].strip("'").strip('"'), condition[0]) and True  # 将where语句中的第二个参数和，第一个参数进行正则比较。如果执行正常就返回True
    else:
        return eval(' '.join(condition))  # 除此使用eval进行python的逻辑判断
