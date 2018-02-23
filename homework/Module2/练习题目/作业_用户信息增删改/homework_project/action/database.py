# -*- coding: utf-8 -*-
title = 'id,name,age,phone,dept,enroll_date'


def get_title(table):
    """获取列函数。

    获取数据库文件的抬头部分,读取表文件的第一行。
    :param table: 表文件参数。
    :return: 返回一个抬头部分的列表。
    """
    try:
        with open(table, 'r', encoding='utf-8') as rf:
            data = rf.readline().strip('\n')
        return data.split(',')
    except FileNotFoundError as e:
        print(e)
        exit(1)


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
    with open(file=table, mode='w', encoding='utf-8') as wf:
        wf.write(data)
