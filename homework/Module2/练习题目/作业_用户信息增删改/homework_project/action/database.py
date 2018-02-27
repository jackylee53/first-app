# -*- coding: utf-8 -*-
from homework_project.config.syntax import get_title


def read_db(table):
    """读取表文件函数。

    :param table: 表文件参数
    :return: 返回一个包含表文件内容的字典
    """
    title = get_title()
    try:
        list = []
        with open(table, 'r', encoding='utf-8') as rf:
            for line in rf:
                temp_list = []
                if line.rstrip('\n').split(',') == title:
                    continue
                else:
                    for values in line.strip('\n').split(','):
                        if values.isdigit():
                            temp_list.append(int(values))
                        else:
                            temp_list.append(values)
                    list.append(dict(zip(title, temp_list)))
        return list
    except FileNotFoundError as e:
        print(e)
        exit(1)


def write_db(table, data):
    value2 = ''
    for values in data:
        list = []
        for value in values.values():
            if value is int:
                list.append(str(value))
            else:
                list.append(str(value))
        value2 += ','.join(list) + '\n'
    with open(file=table, mode='w', encoding='utf-8') as wf:
        wf.write(value2)
