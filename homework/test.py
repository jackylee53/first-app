class Mymeta(type): #继承默认元类的一堆属性
    def __init__(self,class_name,class_bases,class_dic):
        if not class_name.istitle():
            raise TypeError('类名首字母必须大写')

        super(Mymeta,self).__init__(class_name,class_bases,class_dic)

    def __call__(self, *args, **kwargs):
        #self=People
        print(self,args,kwargs) #<class '__main__.People'> ('egon', 18) {}

        #1、实例化People，产生空对象obj
        obj=object.__new__(self)
        print(obj)


        #2、调用People下的函数__init__，初始化obj
        self.__init__(obj,*args,**kwargs)


        #3、返回初始化好了的obj
        return obj

class People(object,metaclass=Mymeta):
    country='China'

    def __init__(self,name,age):
        print('haha123')
        self.name=name
        self.age=age
        print('haha123')

    def talk(self):
        print('%s is talking' %self.name)

obj=People('egon',haha=18)  # People.__call__（People, 'egon', 18）
print(obj.__dict__) #{'name': 'egon', 'age': 18}