class Company:  # 父类
    name = 'Company' # 父类的name数据属性
    def transaction(self):  # 类的函数属性，转账
        print("Transaction monry to your Comany")
        self.purchase()  # 调用实例的采购函数


    def purchase(self):  # 类的函数属性，采购
        print("Your Comany can purchase something.")


class Baidu(Company):  # Baidu类继承Company父类
    name = 'Baidu'  # 派生一个自己的数据属性
    def purchase(self):  # 派生一个自己的采购函数属性
        print("My Comany can purchase Phone.")

    def website(self):  # 派生一个自己专用的website函数属性。父中没有
        print("www.badiu.com")


baidu = Baidu()  # 使用中国类创建一个百度的实例
baidu.website()
print(Baidu.mro())