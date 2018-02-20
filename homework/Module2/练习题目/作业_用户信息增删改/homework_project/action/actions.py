# -*- coding: utf-8 -*-
from .database import read_db


def actions(sql_type, dict_sql):
    dir()
    actions_dict = {'select': select_action,
                    'add': add_action,
                    'del': del_action,
                    'update': update_action,
                    'help': help_action,
                   }
    if sql_type in actions_dict:
        actions_dict[sql_type](dict_sql)


def select_action(dict_sql):
    print(dict_sql)
    print('select')


def add_action(dict_sql):
    print(get_table(dict_sql))
    data = read_db(get_table(dict_sql))



def del_action(dict_sql):
    print(dict_sql)
    pass



def update_action(dict_sql):
    print(dict_sql)
    pass


def help_action(dict_sql):
    print(dict_sql)
    pass


def get_table(dict_sql):
    return 'homework_project/%s' % dict_sql['from'][0]
