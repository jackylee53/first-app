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
    :param output: 导入函数的输出内容。
    :return:
        返回字符。
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
    """

    :param account:
    :param shopping_record:
    :return:
    """

    if shopping_record is None:
        pass
    else:
        data = _load_database()
        data[account]['history'].append(shopping_record)
        _dump_database(data=data)


def _get_shopping_history(account):
    """

    :param account:
    :return:
    """
    data = _load_database()[account]['history']
    return data


def _set_balance(account, price):
    """计算余额函数

    :param account:
    :param price:
    :return:
    """
    if price is None:
        pass
    else:
        data = _load_database()
        data[account]['balance'] -= price
        _dump_database(data=data)

def _recharge_balance(account, price):
    """计算余额函数

    :param account:
    :param price:
    :return:
    """
    data = _load_database()
    data[account]['balance'] += price
    _dump_database(data=data)


def _get_balance(account):
    """获取余额函数

    :param account:
    :return:
    """
    data = _load_database()[account]['balance']
    return data


def _set_lock_user(account, lock_id):
    """

    :param account:
    :param lock_id:
    :return:
    """
    data = _load_database()
    data[account]['lock_status'] = lock_id
    _dump_database(data=data)


def _get_lock_user(account):
    """

    :param account:
    :return:
    """
    data = _load_database()[account]['lock_status']
    return data


def _get_goods(goods=goods_lists):
    """

    :param goods:
    :return:
    """

    # 如果goods参数为"all"，将打印出所有字典中的商品。
    if goods == goods_lists:
        goods_show = ['%s商品列表%s\n' % ('-' * 20, '-' * 20)]
        for g in goods_lists:
            goods_show.append('商品名称：%s, 商品价格：%s\n' % (g['name'], g['price']))
        goods_table = ''.join(goods_show)
        print(goods_table)
    # 当goods参数为其他时，返回该商品的编号，名称，和价格
    else:
        for g in goods_lists:
            if goods == g.get('name'):
                return g
                break


def _login():
    count = 3
    while 1 <= count <= 3:
        user = input('请输入您的用户名：').strip()
        passw = input('请输入您的密码：').strip()
        if not user or not passw:
            continue
        count -= 1
        if user in user_dict.keys() and _get_lock_user(account=user) == 1:
            print(_output_format(output="您的%s账号已被锁定，请联系管理员解锁，或者使用其他账号。" % user))
        elif user in user_dict.keys():
            if passw == user_dict[user]['pass']:
                _set_lock_user(account=user, lock_id=0)
                print(_output_format(output="欢迎 %s 登录!" % user))
                return user
            else:
                print(_output_format(output='密码错误。您还有%s次机会。'% count))
                if count == 0:
                    _set_lock_user(account=user, lock_id=1)
                    exit(1)
                continue
        else:
            print(_output_format(output='用户名错误'))
            continue


def _shopping_buy(account):
    while True:
        _get_goods()
        buy_goods = input('请选择你需要购买的商品("b"返回上一级、"q"退出)：').strip()
        if not buy_goods:
            continue
        elif buy_goods == 'q':
            exit()

        elif buy_goods == 'b':
            break

        else:
            g_goods = _get_goods(goods=buy_goods)
            print(g_goods)
            if _get_balance(account=account) == 0:
                print(_output_format(output='您没有可用的余额，请在上级菜单进行充值！'))
                break
            elif g_goods is None:
                print(_output_format(output='您选购的商品并未在我们的货架中...'))
            else:
                g_price = g_goods.get('price')
                g_balance = _get_balance(account=account)
                _set_shopping_history(account=account, shopping_record=g_goods)
                _set_balance(account=account, price=g_price)
                print(_output_format(output='您当前的余额有%s元' % g_balance))


def _shopping_recharge(account):
    while True:
        recharge = int(input('请输入你需要充值的金额("b"返回上一级、"q"退出)：').strip())
        if recharge == 'q':
            exit()

        elif recharge == 'b':
            break

        else:
            _recharge_balance(account=account, price=recharge)
            balance = _get_balance(account=account)
            print(_output_format(output='您已完成充值！您的当前余额为%s' % balance))
            break


def _shopping(account):
    """购物主菜单函数。

    :param account #导入用户名,用于本函数可以记录用户的购买历史和余额:
    :return:
    """
    # 一级循环。用于用户进入购买界面、查询历史记录和退出登录
    while True:
        choose = input('"r"充值、"s"购买商品、"l"查看购物记录、"q"退出：').strip()
        if choose == 'q':
            exit(0)

        elif choose == 'l':
            # print(_output_format('，'.join(_get_shopping_history(account=account))))
            print(_output_format(_get_shopping_history(account=account)))
            continue

        elif choose == 's':
            _shopping_buy(account=account)

        elif choose == 'r':
            _shopping_recharge(account=account)
            # _set_balance()


def main():
    login = _login()
    _shopping(account=login)
    print(_load_database())


if __name__ == '__main__':
    main()