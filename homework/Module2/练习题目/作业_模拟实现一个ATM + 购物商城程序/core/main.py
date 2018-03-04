#!_*_coding:utf-8_*_
# __author__:"Henry Yuan"

""""
main program handle module , handle all the user interaction stuff

"""

from core import auth
from core import logger
from core import accounts
from core import transaction
from core.auth import login_required
import time

# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')


# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}


@login_required
def account_info(acc_data):
    back_flag = False
    info_temp_list = []
    account_data = acc_data['account_data']
    info_list = ['name', 'age', 'phone', 'enroll_date', 'expire_date', 'account', 'credit', 'balance']
    for i in info_list:
        info_temp_list.append(str(account_data[i]))
    info = ''' --------- BALANCE INFO --------
        username :    {0}
        age:          {1}
        phone:        {2}
        enroll date:  {3}
        expire date:  {4}
        card number:  {5}
        credit:       {6}
        balance:      {7}
        '''.format(*info_temp_list)
    print(info)
    while not back_flag:
        input_b = input("\033[33;1mInput 'b' return to menu:\033[0m").strip()
        if input_b == 'b':
            back_flag = True


@login_required
def repay(acc_data):
    """
    print current balance and let user repay the bill
    :return:
    """
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    {0}
        Balance:    {1}'''.format(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

        if repay_amount == 'b':
            back_flag = True


@login_required
def withdraw(acc_data):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance= ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) >0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


@login_required
def transfer(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance= ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) >0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


@login_required
def pay_check(acc_data):
    pass


@login_required
def logout(acc_data):
    auth.acc_logout(user_data, access_logger)


def interactive(acc_data):
    """ 交互式主页界面

    :param acc_data: 返回的用户账号的具体信息
    :return:
    """
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  账户信息(功能已实现)
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账
    5.  账单
    6.  退出(功能已实现)
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")



def run():
    """
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    acc_data = auth.acc_login(user_data, access_logger)
    # print(acc_data)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)
