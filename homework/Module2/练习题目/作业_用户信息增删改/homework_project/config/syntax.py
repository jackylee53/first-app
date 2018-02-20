#from homework_project.action.actions import actions


def syntax(sql_type):
    syntax_dict = {'select': select_syntax,
                   'add': add_syntax,
                   'del': del_syntax,
                   'update': update_syntax,
                   'help': help_syntax,
                   }
    if sql_type == 'all':
        return syntax_dict
    elif sql_type in syntax_dict:
        return syntax_dict[sql_type](sql_type)


def select_syntax(sql_type):
    select_dict = {'select': [],
                   'from': [],
                   'where': [],
                   #'action': actions(sql_type)
                   }
    return select_dict


def add_syntax(sql_type):
    add_dict = {'add': False,
                'from': [],
                'values': [],
                #'action': actions(sql_type)
                }
    return add_dict


def del_syntax(sql_type):
    del_dict = {'del': False,
                'from': [],
                'where': [],
                #'action': actions(sql_type)
                }
    return del_dict


def update_syntax(sql_type):
    update_dict = {'update': [],
                   'set': [],
                   'where': [],
                   #'action': actions(sql_type)
                   }
    return update_dict


def help_syntax(sql_type):
    help_dict = {'help': [],
                 #'action': actions(sql_type)
                 }
    return help_dict
