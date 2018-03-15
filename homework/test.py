import settings
import hashlib
import time

class People:
    def __init__(self, name, age, sex):
        self.id = self.create_id()  # 每个对象都可以调用create_id非绑定方法，生成ID。并作为自己的属性
        self.name = name
        self.age = age
        self.sex = sex

    def tell_info(self):  # 绑定给对象的方法
        obj_info = """-------PEOPLE INFO--------
        ID:      %s
        Name:    %s
        Age:     %s
        Sex:     %s 
        """ % (self.id, self.name, self.age, self.sex)
        print(obj_info)

    @classmethod
    def import_conf(cls):
        obj = cls(settings.name, settings.age, settings.sex)  # 产生obj对象的类，由cls参数导入。
        return obj  # 返回这个对象


    @staticmethod
    def create_id():  # 非绑定方法，代码内部并不需要对象和类传递进来。
        id = hashlib.md5(str(time.time()).encode('utf-8'))  # 计算MD5值。
        return id.hexdigest()


# 绑定给对象的方法，就应该对象来调用
henry = People('henry', 29, 'man')
henry.tell_info()
# 绑定给类的方法，就应该类来调用。
jerry = People.import_conf()
jerry.tell_info()
# 非绑定方法，不与类和对象绑定，谁都可以调用。