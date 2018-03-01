## README
#### **功能描述**
作业需求：

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
示例代码https://github.com/triaquae/py3_training/tree/master/atm
简易流程图：https://www.processon.com/view/link/589eb841e4b0999184934329注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码！

#### **流程图**
程序流程图
![](https://github.com/henryyuan/first-app/tree/master/homework/Module2/练习题目/作业_用户信息增删改/作业_用户信息增删改.png.png)

#### **程序目录结构**
````text
homework_project
├── action
│   ├── database.py  # 对数据库中的表文件进行操作
│   ├── __init__.py
├── config
│   ├── __init__.py
│   └── syntax.py  # 配置文件。
├── core
│   ├── actions.py  # 对不同的sql类型进行对应的操作
│   ├── help.py  # 提供帮助
│   ├── __init__.py
│   ├── main.py  # 主函数，提供用户输入界面。并执行语法解析与sql操作
│   ├── parsers.py  # 语法解析函数。对用户输入的语法正确性镜像解析，并最终解析成字典格式
├── database
│   └── staff_table  # 表
├── __init__.py
__init__.py 
mysql_run.py  # 执行程序
````
    
### Setup
启动命令。
```text
python mysql_run.py
```

### Credits
    - 作者：henryyuan
    - 日期：2018/03/01
    - 版本：Version 1.0
    - 工具：PyCharm 2017.3.3
    - 版本：Python 3.6.4
    - MarkDown工具：pycharm
    - 流程图工具：ProcessOn
    
### News
    无

### History
    2018-3-1 Version：1.0
