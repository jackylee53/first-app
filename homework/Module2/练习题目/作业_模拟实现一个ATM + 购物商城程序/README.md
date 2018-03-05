## README
#### **功能描述**
作业需求：
```text
1、额度 15000或自定义
2、实现购物商城，买东西加入购物车，调用信用卡接口结账
3、可以提现，手续费5%
4、支持多账户登录
5、支持账户间转账
6、记录每月日常消费流水
7、提供还款接口
8、ATM记录操作日志
9、提供管理接口，包括添加账户、用户额度，冻结账户等。。。
10、用户认证用装饰器
```

注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码！

#### **流程图**
程序流程图
![](https://github.com/henryyuan/first-app/tree/master/homework/Module2/练习题目/作业_用户信息增删改/作业_用户信息增删改.png.png)

#### **程序目录结构**
````text
bin
├── atm.py  # atm入口
├── __init__.py
└── manage.py  # 管理入口
conf
├── __init__.py
└── settings.py  # 配置文件
core
├── accounts.py  # 账号添加、修改额度、禁用、启动接口
├── actions.py   # sql动作接口
├── auth.py      # 用户认证接口
├── database.py  # 数据库操作接口
├── db_handler.py# 无用到
├── __init__.py
├── logger.py    # 日志接口
├── main.py      # 主接口
├── parsers.py   # sql语法解析接口
└── transaction.py # 交易接口
db
├── accounts_table  # 用户账号表
└── managers_table  # 管理员账号表
log
├── access.log      #访问日志
└── transactions.log #交易日志

````
    
### Setup
启动命令。
```text
python atm.py
python manage.py
```

### Credits
    - 作者：henryyuan
    - 日期：2018/03/05
    - 版本：Version 1.0
    - 工具：PyCharm 2017.3.3
    - 版本：Python 3.6.4
    - MarkDown工具：pycharm
    - 流程图工具：ProcessOn
    
### News
    无

### History
    2018-3-5 Version：1.0
