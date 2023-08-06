from unittest import TestCase

from XsCore import Logger


class LoggerTest(TestCase):

    def testLog(self):
        log = Logger("logs/xs_core.log")
        indexs = 0
        while indexs < 1000:
            log.info(f"fadfadf{indexs}")
            indexs += 1
