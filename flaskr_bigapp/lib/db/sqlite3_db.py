from peewee import *
from flaskr_bigapp.lib.sys.configuration import Config_read
from flaskr_bigapp.lib.sys.make import GET,CREATE
from flaskr_bigapp.lib.sys.logger import Logger
from datetime import datetime
from flaskr_bigapp.lib.ops.play_devops import db as devops_db

class BaseModel(Model):
    class Meta:
        database = devops_db

class Playbooks_Record(BaseModel):
    id = PrimaryKeyField(unique=True)
    playbooks = CharField()
    ssh_user = CharField()
    project_name = CharField()
    extra_vars = CharField()
    forks = IntegerField()
    tags = CharField()
    time = DateTimeField()
    class Meta:
        pass;

    def create_tables(self):
        self.database.connect()
        self.database.create_tables([Playbooks_Record])

    def insert_tables(self,playbooks,ssh_user,project_name,extra_vars,forks,tags,time):
        insert = Playbooks_Record(playbooks=playbooks,ssh_user=ssh_user,project_name=project_name,extra_vars=extra_vars,forks=forks,tags=tags,time=time)
        insert.save()


if __name__ == '__main__':
    test = Playbooks_Record()
    test.insert_tables(playbooks='/etc/',ssh_user='root',project_name='test',extra_vars={'hostlist':'fuck'},forks=20,tags=['fuck'],time=datetime(2017,1,15))