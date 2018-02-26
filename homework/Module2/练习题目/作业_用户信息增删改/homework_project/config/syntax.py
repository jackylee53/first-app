def get_title():
    title_dict = ['id','name','age','phone','dept','enroll_date']
    return title_dict


def syntax(sql_type):
    syntax_dict = {'select': select_syntax,
                   'add': add_syntax,
                   'del': del_syntax,
                   'update': update_syntax,
                   }
    if sql_type == 'all':
        return syntax_dict
    elif sql_type in syntax_dict:
        return syntax_dict[sql_type](sql_type)


def select_syntax(sql_type):
    select_dict = {'select': [],
                   'from': '',
                   'where': [],
                   }
    return select_dict


def add_syntax(sql_type):
    add_dict = {'add': False,
                'to': '',
                'values': [],
                }
    return add_dict


def del_syntax(sql_type):
    del_dict = {'del': False,
                'from': '',
                'where': [],
                }
    return del_dict


def update_syntax(sql_type):
    update_dict = {'update': [],
                   'set': '',
                   'where': [],
                   }
    return update_dict

