# -*- coding:utf-8 -*-
import os
import sys
from collections import namedtuple

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager

from flaskr_bigapp.lib.sys.configuration import Config_read
from flaskr_bigapp.lib.ops.callback import ResultsCollector, PlaybookResultsCollector
from flaskr_bigapp.lib.sys.logger import Logger
from flaskr_bigapp.lib.sys.make import GET,CREATE


class Runner(object):
    def __init__(self,tags,forks,*args, **kwargs):
        self._inventory        = None
        self._variable_manager = None
        self._loader           = None
        self._options          = None
        self.passwords         = None
        self.callback          = None
        self.log_file_name     = 'ansible.log'
        self.forks = forks
        self.tags = tags
        self._unreachable_hosts = dict()
        self.basepath = GET().get_log_dir()
        self.create_dir = CREATE()
        self.__initalizeData()

    def __initalizeData(self):
        '''
        初始化ansible
        '''
        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'diff',
                              'tags',
                              ])
        self.options = Options(connection='smart',
                               remote_user='mds',
                               ack_pass=None,
                               forks=int(self.forks),
                               ask_sudo_pass=False,
                               verbosity=5,
                               module_path=None,
                               become=True,
                               become_method='su',
                               become_user='root',
                               check=None,
                               listhosts=False,
                               listtasks=False,
                               listtags=False,
                               diff=False,
                               syntax=None,
                               tags=self.tags,
                               )
        self.loader = DataLoader()
        self.variable_manager = VariableManager(loader=self.loader)
        self.config_items = Config_read()
        self.log_path = self.create_dir.create_dir(basepath=self.basepath,extra_path=self.config_items.get_value(sections='LOGGER_DIR',key='ANSIBLE_LOG_FILE'))
        self.inventory = InventoryManager(loader=self.loader, sources=self.config_items.get_value(sections='ANSIBLE',key='INVENTORY_CONFIG').split(","))
        self.variable_manager.set_inventory(self.inventory)
        self.passwords = dict(conn_pass='131ABJKL',become_pass='131ABJKL')

    '''
    运行ansible adhoc
    '''
    def run(self,host_lists,module_name,module_args,register):
        self.logger = Logger(logger_name='ansible_adhoc',external_path=self.log_path)
        self.callback = ResultsCollector()
        play_source = dict(
            name = 'Ansible Play',
            hosts = host_lists,
            gather_facts =  'no',
            tasks=[dict(action=dict(module=module_name, args=module_args), register=register)]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback,
            )
            result = tqm.run(play)
        except Exception as e:
            print e
            self.logger.error(message='Ansible adhoc error: %s' %e)
        finally:
            if tqm is not None:
                tqm.cleanup()
    '''
    运行ansible playbook
    '''
    def run_playbook(self, playbooks, ssh_user, project_name, extra_vars={}):
        try:
            self.playbookcallback = PlaybookResultsCollector()
            self.logger = Logger(logger_name='ansible_playbook',external_path=self.log_path)
            self.playbooks = playbooks
            if not os.path.exists(self.playbooks[0]):
                self.logger.error(message="Playbooks '%s' is not exist" %self.playbooks[0])
                sys.exit(1)
            else:
                self.logger.debug(message="Playbooks '%s' is exist" %self.playbooks[0])
            self.ssh_user = ssh_user
            self.project_name = project_name
            self.ack_pass = False
            self.connection = 'smart'
            self.extra_vars = extra_vars
            self.variable_manager.extra_vars = extra_vars

            pb = None
            pb = PlaybookExecutor(
                playbooks            = self.playbooks,
                inventory            = self.inventory,
                variable_manager     = self.variable_manager,
                loader               = self.loader,
                options              = self.options,
                passwords            = self.passwords,
                #tag                  = 'repo'
             )
            pb._tqm._stdout_callback = self.playbookcallback
            result = pb.run()
        except Exception as e:
            print e
            self.logger.critical(message="Ansilbe playbook error:%s" %e )

    def get_adhoc_message(self, status, host, result):
        self.status = 'Status:[%s]'%status
        self.host = ',Remote Host:[%s]'%host
        if result.get('start',None):
            self.start_time = result['start']
        else:
            self.start_time = None
        if result.get('end',None):
            self.end_time = result['end']
        else:
            self.end_time = None
        if self.start_time is not None and self.end_time is not None:
            self.period = ',Period:[%s - %s]' %(self.start_time,self.end_time)
        else:
            self.period = ''
        if result.get('cmd',None):
            self.command = 'Command:[%s]' %result['cmd']
        else:
            self.command = ''
        if result.get('msg', None):
            return_data =result.get('msg').replace("\r\n",",")
        elif result.get('stdout', None):
            return_data = result.get('stdout').replace("\n",",")
        elif result.get('stderr', None):
            return_data = result.get('stderr').replace("\n",",")
        else:
            return_data = result.get('stdout').replace("\n",",")
        self.return_data = ',Result:[%s]' %return_data
        self.message = self.status + self.host + self.period + self.command + self.return_data
        return self.message

    def get_playbook_message(self, status, host, result):
        self.status = 'Status:[%s]'%status
        self.host = ',Remote Host:[%s]'%host
        if result.get('msg',None):
            self.msg = ',Msg:[%s]' %result['msg'].replace("\r\n",",")
        else:
            self.msg = ',Msg:[%s]' %result
        self.playbooks = ',Playbook:[%s]' %self.playbooks[0]
        self.message = self.status + self.host + self.playbooks + self.msg
        return self.message

    '''
    将callback返回的ansible执行结果，打印成日志条目
    '''
    def get_adhoc_result(self):
        self.result_raw = {'Ok':{}, 'Failures':{}, 'Unreachable':{}}
        for host, result in self.callback.host_ok.items():
            status = 'Ok'
            self.get_adhoc_message(status, host, result)
            self.result_raw['Ok'][host] = result
            self.logger.info(message=self.message)
        for host, result in self.callback.host_failed.items():
            status = 'Failures'
            self.get_adhoc_message(status, host, result)
            self.result_raw['Failures'][host] = result
            self.logger.error(message=self.message)
        for host, result in self.callback.host_unreachable.items():
            print self.callback.host_unreachable
            status = 'Unreachable'
            self.get_adhoc_message(status, host, result)
            self.result_raw['Unreachable'][host] = result
            self.logger.error(message=self.message)

    def get_playbook_result(self):
        self.result_raw = {'Unreachable': {}, 'Skipped': {}, 'Ok': {}, 'Changed': {}, 'Failures': {}}
        for host, result in self.playbookcallback.task_ok.items():
            status = 'Ok'
            self.get_playbook_message(status, host, result)
            self.result_raw['Ok'][host] = result
            self.logger.info(message=self.message)

        for host, result in self.playbookcallback.task_skip.items():
            status = 'Skip'
            self.get_playbook_message(status, host, result)
            self.result_raw['Skip'][host] = result
            self.logger.info(message=self.message)

        for host, result in self.playbookcallback.task_failed.items():
            status = 'Failures'
            self.get_playbook_message(status, host, result)
            self.result_raw['Failures'][host] = result
            self.logger.error(message=self.message)

        for host, result in self.playbookcallback.task_unreachable.items():
            status = 'Unreachable'
            self.get_playbook_message(status, host, result)
            self.result_raw['Unreachable'][host] = result
            self.logger.error(message=self.message)

        #for host, result in self.playbookcallback.task_stats.items():
        #    self.logger.info(message=result)

