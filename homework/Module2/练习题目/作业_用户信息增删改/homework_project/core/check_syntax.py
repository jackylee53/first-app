# -*- coding: utf-8 -*-
from .help import help


def check_syntax(sql_type, dict_sql):
    ''' sql语句检查函数。

    :param sql_type:
    :param dict_sql:
    :return:
    '''
    tmp_list = []
    for key in dict_sql:
        tmp_list.append(key)  # 将sql语句字典中所有的关键字缓存在一个列表中
    if not dict_sql[key] and dict_sql[key] is not False:
        return 1, help(sql_type)
    else:
        return 0, dict_sql
