# -*- coding: utf-8 -*-
from .help import help


def check_syntax(sql_type, dict_sql):
    tmp_list = []
    for key in dict_sql:
        tmp_list.append(key)
    if 'where' in tmp_list and len(dict_sql['where']) < 3:
        return help(sql_type)
    elif not dict_sql[key] and dict_sql[key] is not False:
        return help(sql_type)
    else:
        return dict_sql
