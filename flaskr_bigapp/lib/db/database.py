#-*- coding:utf8 -*-
import sqlite3_db
import os
from flask import g, current_app
from flaskr_bigapp.lib.sys.configuration import Config_read
from contextlib import closing
from flaskr_bigapp.lib.sys.make import GET,CREATE
from flaskr_bigapp.lib.sys.logger import Logger

class Database(object):
    def __init__(self,*args,**kwargs):
        self.config_items = Config_read()
        self.basepath = GET().get_db_dir()
        self.create_dir = CREATE()
        '''检查配置文件中的配置项属于绝对路径还是相对路径。并且如果目录不存在自行创建'''
        self.local_path = self.create_dir.create_dir(basepath=self.basepath,extra_path=self.config_items.get_value(sections='DATABASE',key='DATABASE_NAME'))
        self.schema_dir = os.path.join(self.basepath,'schema.sql')

    def connect_db(self):
        return sqlite3_db.connect(self.local_path)

    def create_db(self):
        '''创建sql数据并并当执行完成后自动关闭数据库链接'''
        with closing(self.connect_db()) as db:
            with open(self.schema_dir) as f:
                # cursor（游标），用来执行数据库命令。可以excute数据命令、exeutescript执行脚本。
                db.cursor().executescript(f.read())
            db.commit()
        db.close()



    def insert_db(self,sql):
        db = self.connect_db()
        cur = db.cursor()
        cur.execute(sql)
        db.commit()

    def select_db(self):
        db = self.connect_db()
        cur = db.cursor()
        cur.execute('SELECT * from playbooks_record')
        print cur.fetchall()
        db.close()

    def insert_db_temp(self):
        db = self.connect_db()
        tables = 'playbooks_record'
        dicts = {
            'playbooks': 'test',
            'ssh_user': 'root',
            'project_name': 'test',
            'extra_vars': "{'hostlists':'127.0.0.12'}" ,
            'forks': "20" ,
            'tags': "['fuck']"}
        key_lists = [keys.strip() for keys in dicts.keys()]
        value_lists = [value for value in dicts.values()]
        key_len = len(key_lists)
        value_len = len(value_lists)
        if key_len == value_len:
            return_key = ', '.join(list(key_lists))
            return_value = ', '.join(list(value_lists))
        else:
            print 'fuck'
        for i in range(0,key_len):
            print '?'
        print return_key
        print return_value

        #g.db.execute('INSERT INTO %s (%s) VALUES (?, ?)' %(tables,return_key), [return_value])
        #g.db.commit()




    def query_db(query,args=(),one=False):
        cur = g.db.execute(query,args)
        rv = [dict((cur.description[idx][0],value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    test = Database()
    test.create_db()
    test.insert_db_temp()

    #test.insert_db(sql="'INSERT INTO playbooks_record (playbooks, ssh_user, project_name, extra_vars, forks, tags) VALUES (?, ?, ?, ?, ?, ?)', ['haha','haha','haha','haha','haha','haha']")
    test.select_db()