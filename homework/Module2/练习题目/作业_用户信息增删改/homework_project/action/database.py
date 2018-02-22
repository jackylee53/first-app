# -*- coding: utf-8 -*-
title = 'id,name,age,phone,dept,enroll_date'
import os

def get_title(table):
    try:
        with open(table, 'r', encoding='utf-8') as rf:
            data = rf.readline().strip('\n')
        return data.split(',')
    except FileNotFoundError as e:
        print(e)
        exit(1)

def read_db(table):
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
    #os.rename(n_f, f)


if __name__ == '__main__':
    print(get_title('../employee_info'))
    read_db('../employee_info')
