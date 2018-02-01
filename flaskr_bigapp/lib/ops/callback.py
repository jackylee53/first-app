#-*- coding: utf-8 -*-
from ansible.plugins.callback import CallbackBase
from ansible import constants as C

class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok= {}
        self.host_unreachable ={}
        self.host_failed = {}

    def v2_runner_on_ok(self, result,*args,**kwargs):
        host = result._host.get_name()
        self.host_ok[host] = result._result

    def v2_runner_on_unreachable(self, result,*args,**kwargs):
        host = result._host.get_name()
        #print result._result
        self.host_unreachable[host] = result._result

    def v2_runner_on_failed(self, result,*args,**kwargs):
        host = result._host.get_name()
        self.host_failed[host] = result._result

class PlaybookResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(PlaybookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_unreachable = {}
        self.task_skip = {}
        self.task_failed = {}
        self.task_changed = {}
        self.task_stats = {}

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s
        self.task_stats = summary

    def v2_runner_on_ok(self, result, *args, **kwargs):
        host = result._host.get_name()
        self.task_ok[host] = result._result

    def v2_runner_on_skipped(self, result, *args, **kwargs):
        if C.DISPLAY_SKIPPED_HOSTS:
            host = result._host.get_name()
            self.task_skip[host] = result._result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host.get_name()
        self.task_failed[host] = result._result

    def v2_runner_on_unreachable(self, result,*args,**kwargs):
        host = result._host.get_name()
        self.task_unreachable[host] = result._result


