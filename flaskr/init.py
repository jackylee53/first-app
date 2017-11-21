#-*- coding: utf8 -*-
#创建一个初始化sqlite3 db文件的python，使用with与contextlib
from contextlib import closing

from flaskr.modules.db import connect_db
from flaskr.flaskr import app


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            #cursor（游标），用来执行数据库命令。可以excute数据命令、exeutescript执行脚本。
            db.cursor().executescript(f.read())
        db.commit()