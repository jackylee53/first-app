# -*- coding: utf-8 -*-
from config.syntax import get_title

def read_db(table):
    """ 读取表文件函数。

    :param table: 表文件参数
    :return: 返回一个包含表文件内容的字典
    """
    title = get_title()
    try:
        main_list = []
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
                    main_list.append(dict(zip(title, temp_list)))
        return main_list
    except FileNotFoundError as e:
        print(e)
        exit(1)


def write_db(table, data):
    """ 写入表文件函数。

    :param table: 表文件参数
    :param data: 导入的数据。为字典格式
    """
    value2 = ','.join(get_title()) + '\n'
    for values in data:
        temp_list = []
        for value in values.values():
            temp_list.append(str(value))
        value2 += ','.join(temp_list) + '\n'
    with open(file=table, mode='w', encoding='utf-8') as wf:
        wf.write(value2)


def print_info(info, **kwargs):
    """ 打印函数。
        用于select语句打印显示

    :param info: select语句中需要显示的类
    :param kwargs: 字典，用于进行操作的原始数据
    :return:
    """
    temp_list = []
    if info == '*':
        for key in kwargs:
            temp_list.append(str(kwargs[key]))
        print(','.join(temp_list))
    else:
        info_list = info.split(',')
        for i in info_list:
            temp_list.append(str(kwargs[i]))
        print(','.join(temp_list))
