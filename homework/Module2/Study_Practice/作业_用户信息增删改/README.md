## README
#### **功能描述**
1. 当然此表你在文件存储时可以这样表示
```text
id,name,age,phone,dept,enroll_date
1,Alex Li,22,13651054608,IT,2013-04-01
2,Jack Wang,28,13451024608,HR,2015-01-07
3,Rain Wang,21,13451054608,IT,2017-04-01
4,Mack Qiao,44,15653354208,Sales,2016-02-01
5,Rachel Chen,23,13351024606,IT,2013-03-16
6,Eric Liu,19,18531054602,Marketing,2012-12-01
7,Chao Zhang,21,13235324334,Administration,2011-08-08
8,Kevin Chen,22,13151054603,Sales,2013-04-01
9,Shit Wen,20,13351024602,IT,2017-07-03
10,Shanshan Du,26,13698424612,Operation,2017-07-02
```
2. 可进行模糊查询，语法至少支持下面3种查询语法:
```text
select name,age from staff_table where age > 22
select * from staff_table where dept = "IT"
select * from staff_table where enroll_date like "2013"
```
2. 可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增语法: 
```text
add to staff_table values Alex Li,25,134435344,IT,2015-10-29
```
3. 可删除指定员工信息纪录，输入员工id，即可删除语法: 
```text
del from staff_table where id = 3
```
4. 可修改员工信息，语法如下:
```text
update staff_table set dept = Market where dept = IT #把所有dept=IT的纪录的dept改成Market
update staff_table set age = 25 where name = Alex Li #把name=Alex Li的纪录的年龄改成25
```
5. 以上每条语名执行完毕后，要显示这条语句影响了多少条纪录。比如查询语句就显示查询出了多少条、修改语句就显示修改了多少条等。
注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码！

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
