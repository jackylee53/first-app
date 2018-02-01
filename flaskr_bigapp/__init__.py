#-*- coding: utf8 -*-
from flask import Flask, g

from flaskr_bigapp.lib.db.database import Database
from flaskr_bigapp.lib.sys.encoding import Encoding

'''
第一步：导入sys模块，使用setdefultencoding函数将笨程序中的输出内容都转换为utf8。防止中文输出时出现乱码报错。
'''
encodeing = Encoding()
encodeing.encoding_app('utf8')
'''
将flask实例定义为一个工厂函数
'''
def create_app(config_object):
    app = Flask(__name__)
    '''
    第三部.flask获取配置的三种方法：
    1.)可以使用config.from_pyfile()调用flask配置文件中的内容作为配置项
    '''
    app.config.from_pyfile(config_object)
    from .views.index import index
    from .views.login import login
    app.register_blueprint(index)
    app.register_blueprint(login, url_prefix='/cmdb')
    '''
    before_request装饰器。在请求之前执行什么命令
    '''
    @app.before_request
    def before_request():
        # g只保存一次请求，并且每个函数都可用
        database = Database('DATABASE') #创建DATABASE类的一个实例
        g.db = database.connect_db()

    @app.teardown_request
    def teardown_request(exception):
        g.db.close()
    return app
