#!_*_coding:utf-8_*_
""""
main program handle module , handle all the user interaction stuff

"""

from core import auth
from core import logger
from core import parsers
from core import transaction
from core.auth import login_required
from core import actions
from conf import settings
from core import accounts
import random
import datetime

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
    """ print account Information

    :param acc_data: account summary
    :return:
    """
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
        Credit :    %s
        Balance:    %s'''.format(account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)


@login_required
def withdraw(acc_data):
    """
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    """
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif withdraw_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)


@login_required
def transfer(acc_data):
    account_data = acc_data['account_data']
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        payee_account = input("\033[33;1mInput payee account:\033[0m").strip()
        if payee_account == 'b':
            back_flag = True
        else:
            base_dir = settings.DATABASE['path']
            sql_str = 'select * from accounts_table where account = %s' % payee_account
            sql_type = sql_str.split()[0]
            dict_sql = parsers.parsers(sql_str, sql_type, base_dir)
            res = actions.actions(sql_type, dict_sql)
            if not res:
                print("\033[31;1mThe payee you entered is not a bank user!\033[0m")
            else:
                payee_account_data = res[0]
                trans_amount = input("\033[33;1mInput transfer amount:\033[0m").strip()
                if len(trans_amount) > 0 and trans_amount.isdigit():
                    new_balance = transaction.make_transaction(trans_logger, account_data, 'transfer', trans_amount)
                    payee_balance = transaction.make_transaction(trans_logger, payee_account_data,
                                                                 'repay', trans_amount)
                    if new_balance:
                        print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
                    if payee_balance:
                        print('''\033[42;1mThe money has come to the payee [%s]\033[0m''' % payee_account)
                elif trans_amount == 'b':
                    back_flag = True
                else:
                    print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % trans_amount)


@login_required
def pay_check(acc_data):
    back_flag = False
    account_id = acc_data['account_id']
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES['transaction'])
    with open(log_file, 'r') as f:
        for i in f:
            if 'account:%s' % account_id in i:
                print(i)
    while not back_flag:
        input_b = input("\033[33;1mInput 'b' return to menu:\033[0m").strip()
        if input_b == 'b':
            back_flag = True


@login_required
def logout(acc_data):
    auth.acc_logout(acc_data, access_logger)


def interactive(acc_data):
    """ Atm interactive main interface

    :param acc_data: account summary
    :return:
    """
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  账户信息(功能已实现)
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账(功能已实现)
    5.  账单(功能已实现)
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


@login_required
def add_account(acc_data):
    exit_flag = False
    # id, name, age, phone, dept, enroll_date, expire_date, account, password, credit, balance, status, pay_day
    while not exit_flag:
        account_name = input("\033[33;1mInput user name:\033[0m").strip()
        if len(account_name) > 0:
            account_name = account_name
        else:
            continue
        account_age = input("\033[33;1mInput user age:\033[0m").strip()
        if len(account_name) > 0 and account_age.isdigit():
            account_age = account_age
        else:
            continue
        account_phone = input("\033[33;1mInput user phone number:\033[0m").strip()
        if len(account_phone) > 0 and account_phone.isdigit() and len(account_phone) == 11:
            account_phone = account_phone
        else:
            continue
        account_dept = input("\033[33;1mInput user dept:\033[0m").strip()
        if len(account_dept) > 0:
            account_dept = account_dept
        else:
            continue
        account = ''.join(str(random.choice(range(10))) for _ in range(5))  # 随机生成5位账号
        password = input("\033[33;1mInput account password:\033[0m").strip()
        if len(password) == 0:
            password = 'abcde'
        else:
            password = password
        account_enroll_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前时间为开通时间
        account_expire_date = (datetime.datetime.now() + datetime.timedelta(days=(3 * 365))).strftime("%Y-%m-%d")  # 3年后为过期时间
        #print(account_enroll_date,account_expire_date)
        account_credit = input("\033[33;1mInput account credit:\033[0m").strip()
        if len(account_credit) == 0:
            account_credit = str(settings.ACCOUNT_DEFAULT['credit'])
        else:
            account_credit = account_credit


        #print(account)
        input_list = [account_name, account_age,account_phone,account_dept,account_enroll_date,account_expire_date,account,password,account_credit,account_credit,'0','22']
        print(input_list)
        commit = input("\033[33;1mCommit account or exit:(Y/N)\033[0m").strip().upper()
        if commit == 'Y':
            accounts.add_account(*input_list)
            exit_flag = True
        else:
            exit_flag = True


@login_required
def change_credit(acc_data):
    """ Change account credit amount

    :param acc_data:
    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                new_credits = input("\033[33;1mInput new credits amount:\033[0m").strip()
                if len(new_credits) > 0 and new_credits.isdigit():
                    accounts.change_account(dis_account, 'credit = %s' % new_credits)
                else:
                    print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % new_credits)
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")



@login_required
def disable_account(acc_data):
    """ Disable account

    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                accounts.change_account(dis_account, 'status = 1')
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")


@login_required
def enable_account(acc_data):
    """ Enable account

    :return:
    """
    exit_flag = False
    while not exit_flag:
        dis_account = input("\033[33;1mInput account:\033[0m").strip()
        if dis_account == 'b':
            exit_flag = True
        elif len(dis_account) > 0:
            if accounts.load_accounts(dis_account):
                accounts.change_account(dis_account, 'status = 0')
            else:
                print("\033[31;1mThe account you entered is not a bank user!\033[0m")



def mg_interactive(acc_data):
    """ Mange interactive main interface

    :param acc_data: 返回的用户账号的具体信息
    :return:
    """
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  添加账号(功能已实现)
    2.  修改额度(功能已实现)
    3.  禁用账号(功能已实现)
    4.  启用账号(功能已实现)
    5.  退出(功能已实现)
    \033[0m'''
    menu_dic = {
        '1': add_account,
        '2': change_credit,
        '3': disable_account,
        '4': enable_account,
        '5': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")

def run(type):
    """
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    if type == 'atm':
        acc_data = auth.acc_login(user_data, access_logger, 'accounts_table')
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            interactive(user_data)
    elif type == 'manage':
        acc_data = auth.acc_login(user_data, access_logger, 'managers_table')
        if user_data['is_authenticated']:
            user_data['account_data'] = acc_data
            mg_interactive(user_data)
