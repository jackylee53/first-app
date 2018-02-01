'''
作业题目（二）：购物车程序
作业需求：
数据结构：
goods =
[
{"name":
"电脑", "price": 1999},
{"name":
"鼠标", "price": 10},
{"name":
"游艇", "price": 20},
{"name":
"美女", "price": 998},
......
]
功能要求：
基础要求：
1、启动程序后，输入用户名密码后，让用户输入工资，然后打印商品列表
2、允许用户根据商品编号购买商品
3、用户选择商品后，检测余额是否够，够就直接扣款，不够就提醒
4、可随时退出，退出时，打印已购买商品和余额
5、在用户使用过程中，
关键输出，如余额，商品已加入购物车等消息，需高亮显示
扩展需求：
1、用户下一次登录后，输入用户名密码，直接回到上次的状态，即上次消费的余额什么的还是那些，再次登录可继续购买
2、允许查询之前的消费记录
'''
import time,os
class User_Login(object):
    #初始化参数
    def __init__(self):
        self.user_list = ['henry','tom','jenry']
        self.pass_list = ['henry123','tom123','jenry123']
        self.goods =[
            {"name":"电脑", "price": 1999},
            {"name":"鼠标", "price": 10},
            {"name":"游艇", "price": 20},
            {"name":"美女", "price": 998},
        ]
        self.lock_file = '/tmp/lock_file'
    #读取锁定文件函数
    def read_lock(self,file):
        rf = open(self.lock_file,"r")
        return rf.read()

    #写入锁定文件函数
    def write_lock(self,status):
        wf = open(self.lock_file,"w")
        #通过函数外部变量的导入，来判断登录是否成功与失败。失败就在锁定文件中输入1，成功就在锁定文件中输入0
        if status == 0:
            wf.write('0')
        else:
            wf.write('1')

    def login(self):
        #判断锁定文件的值，如果为1。锁定5秒后恢复再次登录的权限。
        if self.read_lock() == '1':
            print('Your account is locked! Please wait 5 second.')
            time.sleep(5)
            self.write_lock(status=0)
        else:
        #如果锁定文件不为1,。要求用户输入账号和密码
            count = 0
            while count < 3:
                user = input("请输入您的用户名: ")
                passw = input("请输入您的密码: ")
                count += 1
                if user in self.user_list:
                    index = self.user_list.index(user)
                    if passw == self.pass_list[index]:
                        self.write_lock(status=0)
                        print('欢迎 %s 登录!'%user)
                        self.login_user = user
                        return 'login'
                        break
                    else:
                        self.write_lock(status=1)
                        print('密码错误!')
                        continue
                else:
                    self.write_lock(status=1)
                    print('用户名错误!')
                    continue
    def commodity(self):
        cart = []
        cache_dict = {}
        while True:
            #判断是否有缓存的用户购物车记录。有的话直接跳过输入工作。直接用余额继续购买
            if os.path.exists('/tmp/%s_cart.txt'%self.login_user):
                rf = open('/tmp/%s_cart.txt'%self.login_user,'r')
                history_dict = eval(rf.read())
                history_cart = history_dict['name']
                print('\033[1m购买商品历史记录:')
                for item in history_cart:
                    print(item)
                print('当前余额%s\033[0m'%history_dict['balance'])
                int_salary = history_dict['balance']
            else:
                #如果用户第一次登录，就请输入工资。并且判断输入的工资必须是数字字符串。不能是其他。否则重新要求输入
                salary = input("请输入你的工资: ")
                if not salary: continue
                elif not salary.isdigit():
                    print('必须输入数字！')
                    continue
                else:
                    history_cart = []
                    int_salary = int(salary)
            #展示goods列表中的商品
            print('商品信息如下：')
            for list in self.goods:
                print(list)
            #用户输入商品的名称，也可以按q退出
            while True:
                commodity = input('请输入者商品名称。退出输入q：').strip()
                if not commodity: continue
                for list in self.goods:
                    if commodity == list['name']:
                        #判断用户输入的商品是否大于它的工资。如果大于不让购买。除此放入购物车。
                        if int_salary < list['price']:
                            print('你的工资不能购买该商品,请重新选择!')
                            continue
                        else:
                            while True:
                                #请用户确认是否需要购买。输入Y后，进行余额计算和历史记录。输入N退出循环，重新输入商品名称。
                                correct = input('\033[1m%s已加入购物车！是否确认购买[Y/N]\033[0m'%commodity).strip()
                                if not correct:
                                    continue
                                elif correct.upper() == 'Y':
                                    cart.append(list)
                                    int_salary  -= list['price']
                                    history_cart.extend(cart)
                                    cache_dict['name'] = history_cart
                                    cache_dict['balance'] = int_salary
                                    wf = open('/tmp/%s_cart.txt'%self.login_user, 'w')
                                    wf.write(str(cache_dict))
                                    print('\033[1m你的余额%s\033[0m'%int_salary)
                                    break
                                elif correct.upper() == 'N':
                                    break

                if commodity == 'q':
                    if len(cart) != 0:
                        print('\033[1m本次购买商品记录:')
                        for item in cart:
                            print(item)
                    else:
                        print('你没有购买任何商品。')
                    print('当前余额%s\033[0m' % int_salary)
                    exit()


if __name__ == '__main__':
    homework = User_Login()
    if homework.login() == 'login':
        homework.commodity()