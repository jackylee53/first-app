# -*- coding: utf-8 -*-
from .database import read_db, get_title, write_db


def actions(sql_type, dict_sql):
    dir()
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action,
                    'help': help_action,
                   }
    if sql_type in actions_dict:
        actions_dict[sql_type](dict_sql)


def select_action(dict_sql):
    if dict_sql['where']:
        pass
        #where_action()
    print('select')


def add_action(dict_sql):
    table_file = get_table(dict_sql)
    title = get_title(table_file)
    value = dict_sql['values']
    data = read_db(table_file)  # 获取原始数据库文件中的所有数据
    id = str(int(data[-1]['id']) + 1)  # 获取原始数据库文件中id列最后一行的id数值，并每次自动+1
    value.insert(0,id)  # 将添加的id插入到value变量中
    if len(value) != len(title):  # 判断输入值得长度是否等于数据库列的长度
        print('值的数量错误')
    else:
        data.append(dict(zip(title,value)))  # 在获取的原始数据中插入行的数据
        value2 = ''
        for i in data:
            value2 += ','.join(i.values()) + '\n'
        write_db(table_file, value2)


def del_action(dict_sql):
    if dict_sql['where']:
        result = where_action(dict_sql['where'], get_table(dict_sql))
    for i in read_db(get_table(dict_sql)):
        for j in result:
            if j != i:
                data.append

    pass



def update_action(dict_sql):
    print(dict_sql)
    pass


def help_action(dict_sql):
    print(dict_sql)
    pass


def where_action(where_sql, table):
    temp_list1 = []
    if where_sql[1] == '=':
        data = read_db(table)
        for item in data:
            if item[where_sql[0]] == where_sql[2]:
                temp_list1.append(item)
        return temp_list1



def get_table(dict_sql):
    return 'homework_project/%s' % dict_sql['from'][0]


