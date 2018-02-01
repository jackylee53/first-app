from flaskr_bigapp.lib.ops.runner import Runner
from flaskr_bigapp.lib.sys.configuration import Config_read
from flaskr_bigapp.lib.sys.configuration import Config_read
from flaskr_bigapp.lib.sys.make import GET,CREATE
from peewee import SqliteDatabase
from datetime import datetime
import json

config_items = Config_read()
basepath = GET().get_db_dir()
create_dir = CREATE()
db = SqliteDatabase(create_dir.create_dir(basepath=basepath, extra_path=config_items.get_value(sections='DATABASE',key='DATABASE_NAME')))

class Play(object):
    def __init__(self,*args,**kwargs):
        pass;

    def play_adhoc(self,hosts,module_name,module_args,register='result',forks=int(Config_read().get_value(sections='ANSIBLE',key='FORKS')),tags=[]):
        self.play = Runner(forks=forks,tags=tags)
        self.host_lists = hosts
        self.module_name = module_name
        self.module_args = module_args
        self.register = register
        self.play.run(self.host_lists,module_name,module_args,register)
        result = self.play.get_adhoc_result()

    def play_playbook(self,extra_vars,playbooks,forks=int(Config_read().get_value(sections='ANSIBLE',key='FORKS')),ssh_user = 'root',project_name = 'ansible',tags = []):
        self.playbooks = [playbooks]
        self.forks = forks
        self.tags = tags
        self.ssh_user = ssh_user
        self.project_name = project_name
        self.tags = tags
        self.extra_vars = extra_vars
        from flaskr_bigapp.lib.db.sqlite3_db import Playbooks_Record
        self.playbooks_record = Playbooks_Record()
        self.play = Runner(forks=self.forks,tags=self.tags)
        self.play.run_playbook(playbooks=self.playbooks,
                    ssh_user=self.ssh_user,
                    project_name=self.project_name,
                    extra_vars=self.extra_vars
                    )
        result = self.play.get_playbook_result()
        dict = {'playbooks':self.playbooks,'ssh_user':self.ssh_user,'project_name':self.project_name,'extra_vars':self.extra_vars,'forks':self.forks,'tags':self.tags}

        test=json.dumps(dict,sort_keys=True,indent = 4,separators=(',', ': '),encoding="utf8",ensure_ascii=True )
        print test
        self.playbooks_record.insert_tables(playbooks=self.playbooks,ssh_user=self.ssh_user,project_name=self.project_name,extra_vars=self.extra_vars,forks=self.forks,tags=self.tags,time=datetime(2015,1,12))



if __name__ == "__main__":
    test = Play()
    test.play_adhoc(hosts=['127.0.0.1'],
             module_name='shell',
             module_args='ls /',
             register='result',
             forks=20
    )
    test.play_playbook(playbooks='/root/auto-configure-change/auto-create-repo/auto-create-repo.yml',
                       extra_vars={'hostlists':'127.0.0.12'},
                       tags=['fuck'],
                       forks=20
    )

