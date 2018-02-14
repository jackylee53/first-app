# -*- coding: utf-8 -*-
def select_parses(sql_list):
    dict_sql = {'select': [],
                'from': [],
                'where': [],
                'like': [],
                }
    test = 'select name,age from staff_table where age > 22'
    list = test.split(' ')
    print(list)
    for i in list:
        if i in dict_sql:
            key = i
        else:
            dict_sql[key].append(i)

    print(dict_sql)