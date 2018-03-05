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
程序流程图（待补全）
![]()

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
    
#### 启动命令
启动命令。
```text
python atm.py
python manage.py
```

#### 发布信息
    - 作者：henryyuan
    - 日期：2018/03/05
    - 版本：Version 1.0
    - 工具：PyCharm 2017.3.3
    - 版本：Python 3.6.4
    - MarkDown工具：pycharm
    - 流程图工具：ProcessOn
    
#### 新闻
    无

#### 历史记录
    2018-3-5 Version：1.0
    
#### 遇到的问题：
```text
1.) 在main.py接口中的add_account()函数。用于添加账号。需要输入多个input条件。代码如下：
```
```python
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
```
```text
每个input语句都需要有if的判断，但当有多个input输入语句时，就会出现过多的重复的if代码。如何减少if语句的代码量。
```