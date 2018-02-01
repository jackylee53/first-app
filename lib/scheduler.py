from apscheduler.schedulers.background import BackgroundScheduler
import time,os
class Schedulers(object):
    def background(self,job,week,hour,minute,second):
        sched = BackgroundScheduler()
        #sched.add_job(job, 'interval',seconds=3)
        sched.add_job(job, 'cron', day_of_week=week, hour=hour, minute=minute, second=second)
        sched.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            sched.shutdown()