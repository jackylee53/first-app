# -*- coding: utf-8 -*-
title = 'id,name,age,phone,dept,enroll_date'


def read_db(table):
    temp_list = []
    with open(table, 'r', encoding='utf-8') as rf:
        for line in rf:
            temp_list.append(dict(zip(title.split(','), line.split(','))))
    return temp_list


def write_db(table, *args, **kwargs):
    with open(table, 'w', encoding='utf-8') as wf:
        data = wf.write(*args)


if __name__ == '__main__':
    read_db('../employee_info')
