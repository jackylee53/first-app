# -*- coding: utf8 -*-
import json

user_dict = {'henry': {'pass': 'henry123'},
             'tom': {'pass': 'tom123'},
             'jenry': {'pass': 'jenry123'}}
goods_lists = [
    {'name': '电脑', 'price': 1999},
    {'name': '鼠标', 'price': 10},
    {'name': '游艇', 'price': 20},
    {'name': '美女', 'price': 998},
]
database_file = 'database.json'


def _setup():
    """
    安装函数，主要用于初始化database.json文件。无其他用途
    """
    data = {}
    for account in user_dict:
        data[account] = {}
        data[account]['history'] = []
        data[account]['balance'] = 0
        data[account]['lock_status'] = 0
    _dump_database(data=data)


def _output_format(output):
    """输出内容格式化。

    将输出的内容格式化为高亮显示。
    :param output: 导入需要高亮显示的输出内容。
    :return:
        返回字符串。
    """
    return '\033[1m%s\033[0m' % output


def _load_database(filename=database_file):
    """数据库读取函数。

    读取json文件。该文件存储了用户的购买记录、剩余资金、锁定状态。
    :param filename: 数据库文件，默认为database.json。
    :return:
        将database.json文件中的内容读取后，返回字典。
        例如：
            {"henry": {"history": [], "balance": 0, "lock_status": 0},
             "tom": {"history": [], "balance": 0, "lock_status": 0},
             "jenry": {"history": [], "balance": 0, "lock_status": 0}}
    """
    with open(filename, 'r') as f:
        database = json.load(f)
    return database


def _dump_database(data, filename=database_file):
    """写入数据库函数。

    将数据回写到数据库文件中。
    :param data: 导入的数据内容。
    :param filename: 数据库文件，默认为database.json。
    """
    with open(filename, 'w') as f:
        json.dump(data, f)


def _set_shopping_history(account, shopping_record):
    """存储购物记录函数

    该函数用于将用户的购物记录。通过调用_dump_database()函数的方式记录到数据库中
    :param account: 导入登录的用户账号
    :param shopping_record: 导入购物的记录
    """
    data = _load_database()
    data[account]['history'].append(shopping_record)
    _dump_database(data=data)


def _get_shopping_history(account):
    """获取历史的购物记录

    该函数调用_load_database()函数和_get_goods()函数。获取历史的购物记录，并进行输出格式化
    :param account: 导入登录的用户账号
    """
    data = _load_database()[account]['history']
    _get_goods(goods=data)


def _set_balance(account, price):
    """计算余额函数

    该函数用于
    :param account: 导入登录的用户账号
    :param price: 导入商品价格
    """
    data = _load_database()
    data[account]['balance'] -= price
    _dump_database(data=data)


def _recharge_balance(account, price):
    """余额充值函数

    :param account: 导入登录的用户账号
    :param price: 导入充值价格
    """
    data = _load_database()
    data[account]['balance'] += price
    _dump_database(data=data)


def _get_balance(account):
    """获取余额函数

    :param account: 导入登录的用户账号
    :return:
        将database.json文件中的'balance'键的值进行读取，返回字符。
    """
    data = _load_database()[account]['balance']
    return data


def _set_lock_user(account, lock_id):
    """设置用户锁

    当用户登录不正确时，触发用户锁定。
    :param account: 导入登录的用户账号
    :param lock_id: 锁定的状态，0为不锁定，1为锁定
    """
    data = _load_database()
    data[account]['lock_status'] = lock_id
    _dump_database(data=data)


def _get_lock_user(account):
    """获取用户锁

    检查database.json文件中lock_status键的值。
    :param account: 导入登录的用户账号
    :return:
        将database.json文件中的'lock_status'键的值进行读取，返回类型为字符串。
    """
    data = _load_database()[account]['lock_status']
    return data


def _get_goods(goods=goods_lists):
    """将商品列表（goods_lists）进行重新格式化

    用于展示商品列表和历史购物记录
    :param goods: 导入商品信息。可以是列表和字符串。
    """

    # 如果goods参数的类型是列表，将打印出所有列表中的商品。并将输出内容重新格式化为：
    # --------------------商品列表--------------------
    # 商品名称：电脑, 商品价格：1999
    # 商品名称：鼠标, 商品价格：10
    # 商品名称：游艇, 商品价格：20
    # 商品名称：美女, 商品价格：998

    if type(goods) == list:
        goods_show = ['%s商品列表%s\n' % ('-' * 20, '-' * 20)]
        for g in goods:
            goods_show.append('商品名称：%s, 商品价格：%s\n' % (g['name'], g['price']))
        goods_table = ''.join(goods_show)
        print(goods_table)
    # 当goods参数为其他时，并且goods等于商品列表中某个商品的名称。返回该商品的字典。
    else:
        for g in goods_lists:
            if goods == g.get('name'):
                return g


def _login():
    """用户登录函数

    :return:
        返回用户登录的账号。返回类型为字符串。
    """
    count = 3
    # 反向计数器，当计数器大于等于1并小于等于3时执行循环。否则退出循环。
    while 1 <= count <= 3:
        user = input('请输入您的用户名：').strip()
        passw = input('请输入您的密码：').strip()
        # 如果用户名和账号输入空格的化重新输入。
        if not user or not passw:
            continue
        # 每执行一次循环，计数器减1。
        count -= 1
        # 如果用户名在user_dict的字典中，并且调用_get_lock_user()函数判断用户账号的锁定状态是否为1。
        # 如果两个条件都满足的话直接打印账号被锁定的信息。
        if user in user_dict.keys() and _get_lock_user(account=user) == 1:
            print(_output_format(output="您的%s账号已被锁定，请联系管理员解锁，或者使用其他账号。" % user))
        # 如果用户名在user_dict的字典中，请用户输入密码。
        elif user in user_dict.keys():
            # 如果密码等于user_dict[user]字典中的'pass'键的值。答应欢迎登陆界面。并设置用户锁为0。
            if passw == user_dict[user]['pass']:
                _set_lock_user(account=user, lock_id=0)
                print(_output_format(output="欢迎 %s 登录!" % user))
                return user
            # 除此答应密码错误，并给出3个输入机会。如果计数器等于0。就设置用户锁为1。
            else:
                print(_output_format(output='密码错误。您还有%s次机会。'% count))
                if count == 0:
                    _set_lock_user(account=user, lock_id=1)
                    exit(1)
                continue
        # 当用户用户名输入错误时，答应错误。并重新要求输入。
        else:
            print(_output_format(output='用户名错误'))
            continue


def _shopping_buy(account):
    """购买函数

    :param account: 导入登录的用户账号
    """
    while True:
        # 展示商品信息。
        _get_goods()
        # 请用户输入需要购买的商品名称
        buy_goods = input('请选择你需要购买的商品("b"返回上一级、"q"退出)：').strip()
        if not buy_goods:
            continue
        # 按'q'退出
        elif buy_goods == 'q':
            exit()
        # 按'b'返回上一层
        elif buy_goods == 'b':
            break

        else:
            g_goods = _get_goods(goods=buy_goods)
            # 判断是否有余额。如果余额为0。要求用户充值。并返回上一层。
            if _get_balance(account=account) == 0:
                print(_output_format(output='您没有可用的余额，请在上级菜单进行充值！'))
                break
            # 判断用户输入的商品是否在商品列表中。如果不在，让用户重新输入。
            elif g_goods is None:
                print(_output_format(output='您选购的商品并未在我们的货架中...'))
                continue
            # 除此，获取商品的售价、添加历史购买记录（调用_set_shopping_history()函数）、计算余额（调用_set_balance()函数）、
            # 打印用户的当前余额。
            else:
                g_price = g_goods.get('price')
                g_balance = _get_balance(account=account)
                _set_shopping_history(account=account, shopping_record=g_goods)
                _set_balance(account=account, price=g_price)
                print(_output_format(output='您当前的余额有%s元' % g_balance))


def _shopping_recharge(account):
    """充值函数

    :param account:导入登录的用户账号
    """
    while True:
        recharge = input('请输入你需要充值的金额("b"返回上一级、"q"退出)：').strip()
        if recharge == 'q':
            exit()

        elif recharge == 'b':
            break

        else:
            if not recharge.isdigit():
                print(_output_format(output='必须输入数值！'))
                continue
            else:
                int_recharge = int(recharge)
                _recharge_balance(account=account, price=int_recharge)
                balance = _get_balance(account=account)
                print(_output_format(output='您已完成充值！您的当前余额为%s' % balance))
                break


def _shopping(account):
    """购物主菜单函数。

    :param account: 导入登录的用户账号
    """
    # 一级循环。用于用户进入购买界面、查询历史记录和退出登录
    while True:
        choose = input('"r"充值、"s"购买商品、"l"查看购物记录、"q"退出：').strip()
        if choose == 'q':
            exit(0)

        elif choose == 'l':
            _get_shopping_history(account=account)
            continue

        elif choose == 's':
            _shopping_buy(account=account)

        elif choose == 'r':
            _shopping_recharge(account=account)


def main():
    login = _login()
    _shopping(account=login)


if __name__ == '__main__':
    main()
