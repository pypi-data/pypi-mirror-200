from datetime import date

from apscheduler.schedulers.blocking import BlockingScheduler


class XsJob(BlockingScheduler):
    # def __init__(self):
    #     pass

    def addJob(self, datetime, fn, fn_args=[]):
        self.add_job(fn, 'date', run_date=datetime, args=fn_args)

    def addTimer_Seconds(self, sds: int, fn, fn_args=None):
        self.add_job(fn, 'interval', seconds=sds, args=fn_args)

    def addTimer_Minutes(self, mins: int, fn, fn_args: []):
        self.add_job(fn, 'interval', minutes=mins, args=fn_args)

