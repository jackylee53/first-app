# -*- coding: utf8 -*-
from .database_json import DatabaseJson

user_dict = {'henry': {'pass': 'henry123'},
             'tom': {'pass': 'tom123'},
             'jenry': {'pass': 'jenry123'}}
database_file = '../database.json'


class UserLogin(object):
    def __init__(self):
        self.db = DatabaseJson()

    def _setup(self):
        """
        安装函数，主要用于初始化database.json文件。无其他用途
        """
        data = {}
        for account in user_dict:
            data[account] = {}
            data[account]['history'] = []
            data[account]['balance'] = 0
            data[account]['lock_status'] = 0
        self.db.dump_database(data=data)

    @staticmethod
    def _output_format(output):
        """输出内容格式化。

        将输出的内容格式化为高亮显示。
        :param output: 导入需要高亮显示的输出内容。
        :return:
            返回字符串。
        """
        return '\033[1m%s\033[0m' % output

    def _set_lock_user(self, account, lock_id):
        """设置用户锁

        当用户登录不正确时，触发用户锁定。
        :param account: 导入登录的用户账号
        :param lock_id: 锁定的状态，0为不锁定，1为锁定
        """
        data = self.db.load_database()
        data[account]['lock_status'] = lock_id
        self.db.dump_database(data=data)

    def _get_lock_user(self, account):
        """获取用户锁

        检查database.json文件中lock_status键的值。
        :param account: 导入登录的用户账号
        :return:
            将database.json文件中的'lock_status'键的值进行读取，返回类型为字符串。
        """
        data = self.db.load_database()[account]['lock_status']
        return data

    def _login(self):
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
            if user in user_dict.keys() and self._get_lock_user(account=user) == 1:
                print(self._output_format(output="您的%s账号已被锁定，请联系管理员解锁，或者使用其他账号。" % user))
            # 如果用户名在user_dict的字典中，请用户输入密码。
            elif user in user_dict.keys():
                # 如果密码等于user_dict[user]字典中的'pass'键的值。答应欢迎登陆界面。并设置用户锁为0。
                if passw == user_dict[user]['pass']:
                    self._set_lock_user(account=user, lock_id=0)
                    print(self._output_format(output="欢迎 %s 登录!" % user))
                    return user
                # 除此答应密码错误，并给出3个输入机会。如果计数器等于0。就设置用户锁为1。
                else:
                    print(self._output_format(output='密码错误。您还有%s次机会。' % count))
                    if count == 0:
                        self._set_lock_user(account=user, lock_id=1)
                        exit(1)
                    continue
            # 当用户用户名输入错误时，答应错误。并重新要求输入。
            else:
                print(self._output_format(output='用户名错误'))
                continue

    def main(self):
        self._login()
