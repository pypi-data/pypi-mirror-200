import os
from unittest import TestCase

from XsCore import XsJob, XsDateUtils





class XsTaskJobTest(TestCase):

    def testTimer(self):
        job = XsJob()
        job.addTimer_Seconds(3, self.__job1, ["这是一个测试"])
        job.start()
        # os.system('pause')

    def __job1(self, txt):
        print(f"结果:{txt} 时间:{XsDateUtils.getNowDateTime()}")