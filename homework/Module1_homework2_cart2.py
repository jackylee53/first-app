import time,os,json
#初始化参数
user_dict = {'henry':{'pass':'henry123'},
             'tom':{'pass':'tom123'},
             'jenry':{'pass':'jenry123'}}
database_file = 'database.json'
data={}
def _output_format(output):
    return """\033[1m%s\033[0m""" %output

def _load_database(filename=database_file):
    """

    :param filename:
    :return:
    """
    with open(filename,"r") as f:
        database = json.load(f)
    return database

def _dump_database(data,filename=database_file,):
    with open(filename,"w") as f:
        json.dump(data,f)

def _setup():
     for account in user_dict:
         data[account] = {}
         data[account]['history'] = []
         data[account]['balance'] = 0
         data[account]['lock_id'] = 0
     _dump_database(data=data)

def _set_shopping_history(account,shopping_record):
    data = _load_database()
    data[account]['history'] = shopping_record
    _dump_database(data=data)

def _get_shopping_history(account):
    data = _load_database()[account]['history']
    return data

def _set_balance(account,price):
    data = _load_database()
    data[account]['balance'] -= price
    _dump_database(data=data)

def _get_balance(account):
    data = _load_database()[account]['balance']
    return data

def _set_lock_user(account,lock_id):
    data = _load_database()
    data[account]['lock_id'] = lock_id
    _dump_database(data=data)

def _get_lock_user(account):
    data = _load_database()[account]['lock_id']
    return data

def _login():
    count = 3
    while count <= 3 and count >= 1:
        user = input("Please input Username: ").strip()
        passw = input("Please input Password: ").strip()
        if (not user or not passw): continue
        count -= 1
        if user in user_dict.keys() and _get_lock_user(account=user) == 1:
            print(_output_format(output="您的%s账号已被锁定，请联系管理员解锁，或者使用其他账号。" %(user)))
        elif user in user_dict.keys():
            if passw == user_dict[user]['pass']:
                _set_lock_user(account=user, lock_id=0)
                print(_output_format(output="欢迎 %s 登录!" %(user)))
                return 'login'
            else:
                print(_output_format(output='密码错误。您还有%s次机会。'%(count)))
                if count == 0:
                    _set_lock_user(account=user, lock_id=1)
                continue
        else:
            print(_output_format(output='用户名错误'))
            continue

def _shopping():
    pass

def main():
    #_setup()
    _login()
    #_set_account()
    #_set_shopping_history(account='henry',shopping_record='1234')
    #_set_balance(account='henry',balance=202)
    #_set_lock_user(account='henry',lock_id=1)
    #print(_get_shopping_history(account='henry'))
    #print(_get_balance(account='henry'))
    print(_load_database())


if __name__ == '__main__':
    main()

# def commodity(self):
#
#         while True:
#             #判断是否有缓存的用户购物车记录。有的话直接跳过输入工作。直接用余额继续购买
#             if os.path.exists('/tmp/%s_cart.txt'%self.login_user):
#                 rf = open('/tmp/%s_cart.txt'%self.login_user,'r')
#                 history_dict = eval(rf.read())
#                 history_cart = history_dict['name']
#                 print('\033[1m购买商品历史记录:')
#                 for item in history_cart:
#                     print(item)
#                 print('当前余额%s\033[0m'%history_dict['balance'])
#                 int_salary = history_dict['balance']
#             else:
#                 #如果用户第一次登录，就请输入工资。并且判断输入的工资必须是数字字符串。不能是其他。否则重新要求输入
#                 salary = input("请输入你的工资: ")
#                 if not salary: continue
#                 elif not salary.isdigit():
#                     print('必须输入数字！')
#                     continue
#                 else:
#                     history_cart = []
#                     int_salary = int(salary)
#             #展示goods列表中的商品
#             print('商品信息如下：')
#             for list in self.goods:
#                 print(list)
#             #用户输入商品的名称，也可以按q退出
#             while True:
#                 commodity = input('请输入者商品名称。退出输入q：').strip()
#                 if not commodity: continue
#                 for list in self.goods:
#                     if commodity == list['name']:
#                         #判断用户输入的商品是否大于它的工资。如果大于不让购买。除此放入购物车。
#                         if int_salary < list['price']:
#                             print('你的工资不能购买该商品,请重新选择!')
#                             continue
#                         else:
#                             while True:
#                                 #请用户确认是否需要购买。输入Y后，进行余额计算和历史记录。输入N退出循环，重新输入商品名称。
#                                 correct = input('\033[1m%s已加入购物车！是否确认购买[Y/N]\033[0m'%commodity).strip()
#                                 if not correct:
#                                     continue
#                                 elif correct.upper() == 'Y':
#                                     cart.append(list)
#                                     int_salary  -= list['price']
#                                     history_cart.extend(cart)
#                                     cache_dict['name'] = history_cart
#                                     cache_dict['balance'] = int_salary
#                                     wf = open('/tmp/%s_cart.txt'%self.login_user, 'w')
#                                     wf.write(str(cache_dict))
#                                     print('\033[1m你的余额%s\033[0m'%int_salary)
#                                     break
#                                 elif correct.upper() == 'N':
#                                     break
#
#                 if commodity == 'q':
#                     if len(cart) != 0:
#                         print('\033[1m本次购买商品记录:')
#                         for item in cart:
#                             print(item)
#                     else:
#                         print('你没有购买任何商品。')
#                     print('当前余额%s\033[0m' % int_salary)
#                     exit()


# if __name__ == '__main__':
#     homework = User_Login()
#     if homework.login() == 'login':
#         homework.commodity()