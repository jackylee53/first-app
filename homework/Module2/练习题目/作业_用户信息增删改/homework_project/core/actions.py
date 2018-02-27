# -*- coding: utf-8 -*-
from homework_project.action.database import read_db, write_db
from homework_project.config.syntax import get_title
import re

def actions(sql_type, dict_sql):
    #data = read_db(table_file)  # 获取原始数据库文件中的所有数据
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action}
    if sql_type in actions_dict:
        return actions_dict[sql_type]


def select_action(dict_sql):
    if dict_sql['where']:
        pass
        #where_action()
    print(dict_sql)
    print('select')


def add_action(dict_sql):
    data = read_db(dict_sql['to'])  # 获取原始数据库文件中的所有数据
    value = dict_sql['values']  # 从dict_sql中获取values的列表
    id = str(int(data[-1]['id']) + 1)  # 获取原始数据库文件中id列最后一行的id数值，并每次自动+1。然后转换为字符串格式
    value.insert(0,id)  # 将添加的id插入到value变量中
    if len(value) != len(get_title()):  # 判断输入值得长度是否等于数据库文件中定义的列的长度
        print('列数不正确')
    else:
        data.append(dict(zip(get_title(),value)))  # 在获取的原始数据中插入行的数据
        write_db(dict_sql['to'], data)


def del_action(dict_sql):
    data = read_db(dict_sql['from'])  # 获取原始数据库文件中的所有数据
    key = dict_sql['where'][0]
    for values in data:
        dict_sql['where'][0] = str(values[key])
        if where_action(dict_sql['where']):
            print(values)
            data.remove(values)
    print(data)
    #write_db(dict_sql['from'], data)



def update_action(dict_sql):
    set_list = dict_sql['set']
    # result = where_action(dict_sql['where'])
    # for j in result:
    #     if j in data:
    #         data[data.index(j)][set_list[0]] = set_list[2]
    # value2 = ''
    # for i in data:
    #      value2 += ','.join(i.values()) + '\n'
    # write_db(table_file, value2)


def where_action(condition):
    if 'like' in condition:
        return re.search(condition[2].strip("'").strip('"'), condition[0]) and True
    else:
        return eval(' '.join(condition))



