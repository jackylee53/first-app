# -*- coding: utf8 -*-

import json

database_file = 'database.json'


class DatabaseJson(object):
    def __init__(self):
        self.filename = database_file

    def load_database(self):
        """数据库读取函数。

        读取json文件。该文件存储了用户的购买记录、剩余资金、锁定状态。
        :return:
            将database.json文件中的内容读取后，返回字典。
            例如：
                {"henry": {"history": [], "balance": 0, "lock_status": 0},
                 "tom": {"history": [], "balance": 0, "lock_status": 0},
                 "jenry": {"history": [], "balance": 0, "lock_status": 0}}
        """
        with open(self.filename, 'r') as f:
            database = json.load(f)
        return database

    def dump_database(self, data):
        """写入数据库函数。

        将数据回写到数据库文件中。
        :param data: 导入的数据内容。
        """
        with open(self.filename, 'w') as f:
            json.dump(data, f)
