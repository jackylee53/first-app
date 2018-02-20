# -*- coding: utf-8 -*-
def help(sql_type):
    dict = {'select': select_help,
            'add': add_help,
            'del': del_help,
            'update': update_help,
            }
    if sql_type in dict:
        return dict[sql_type]()


def select_help():
    strings = '''select语法错误。请查看案例：
    select name,age from staff_table where age > 22
    select * from staff_table where dept="IT"
    select * from staff_table where enroll_date like "2013"
    '''
    return strings


def add_help():
    strings = '''add语法错误。请查看案例：
    add from staff_table Alex Li,25,134435344,IT,2015-10-29
    '''
    return strings


def del_help():
    strings = '''del语法错误。请查看案例：
    del from staff_table where id=3
    '''
    return strings


def update_help():
    strings = '''update语法错误。请查看案例：
    UPDATE staff_table SET dept="Market" WHERE  dept = "IT"
    UPDATE staff_table SET age=25 WHERE  name ="Alex Li"
    '''
    return strings

