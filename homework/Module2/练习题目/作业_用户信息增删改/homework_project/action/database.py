# -*- coding: utf-8 -*-
title = 'id,name,age,phone,dept,enroll_date'


def read_db(table):
    """读取表文件函数。

    :param table: 表文件参数
    :return: 返回一个包含表文件内容的字典
    """
    try:
        temp_list = []
        with open(table, 'r', encoding='utf-8') as rf:
            for line in rf:
                temp_list.append(dict(zip(title.split(','), line.strip('\n').split(','))))
        return temp_list
    except FileNotFoundError as e:
        print(e)
        exit(1)


def write_db(table, data):
    value2 = ''
    for i in data:
        value2 += ','.join(i.values()) + '\n'
    with open(file=table, mode='w', encoding='utf-8') as wf:
        wf.write(value2)
