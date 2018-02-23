# -*- coding: utf-8 -*-
from .database import read_db, get_title, write_db


table_file = ''
title = []
data = []


def actions(sql_type, dict_sql):
    dir()
    global table_file
    table_file = get_table(sql_type, dict_sql)
    global title
    title = get_title(table_file)
    global data
    data = read_db(table_file)  # 获取原始数据库文件中的所有数据
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action,
                    'help': help_action,
                   }
    if sql_type in actions_dict:
        return actions_dict[sql_type](dict_sql)


def select_action(dict_sql):
    if dict_sql['where']:
        pass
        #where_action()
    print(dict_sql)
    print('select')


def add_action(dict_sql):
    value = dict_sql['values']  # 冲dict_sql中获取values的值
    id = str(int(data[-1]['id']) + 1)  # 获取原始数据库文件中id列最后一行的id数值，并每次自动+1。然后转换为字符串格式
    value.insert(0,id)  # 将添加的id插入到value变量中
    if len(value) != len(title):  # 判断输入值得长度是否等于数据库文件中定义的列的长度
        print('values的数量不等于title定义的数量。')
    else:
        data.append(dict(zip(title,value)))  # 在获取的原始数据中插入行的数据
        value2 = ''
        for i in data:
            value2 += ','.join(i.values()) + '\n'
        write_db(table_file, value2)


def del_action(dict_sql):
    result = where_action(dict_sql['where'])
    for j in result:
        data.remove(j)
    value2 = ''
    for i in data:
         value2 += ','.join(i.values()) + '\n'
    write_db(table_file, value2)



def update_action(dict_sql):
    set_list = dict_sql['set']
    result = where_action(dict_sql['where'])
    for j in result:
        if j in data:
            data[data.index(j)][set_list[0]] = set_list[2]
    value2 = ''
    for i in data:
         value2 += ','.join(i.values()) + '\n'
    write_db(table_file, value2)


def help_action(dict_sql):
    print(dict_sql)
    pass


def where_action(where_sql):
    temp_list1 = []
    if '=' in where_sql:
        for item in data:
            if item[where_sql[0]] == where_sql[2]:
                temp_list1.append(item)
        return temp_list1


def get_table(sql_type, dict_sql):
    if sql_type == 'update':
        return 'homework_project/%s' % dict_sql['update'][0]
    else:
        return 'homework_project/%s' % dict_sql['from'][0]


