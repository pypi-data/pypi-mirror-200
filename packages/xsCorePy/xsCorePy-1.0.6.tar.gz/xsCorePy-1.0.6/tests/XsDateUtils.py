import datetime
import time
from unittest import TestCase

from XsCore import XsDateUtils


class XsHttpTest(TestCase):

    def testAddDays(self):
        date = XsDateUtils.add_days(7)
        # date = XsDateUtils.add_date(120, tp='s')
        print(date)

    def testMiniSecond(self):
        s1 = XsDateUtils.get_milli_second()
        print(s1)
        time.sleep(5)
        s2 = XsDateUtils.get_milli_second()
        print(s2)
        s3 = s2 - s1
        self.assertEqual(5000, s3)

    def testSecond(self):
        s1 = XsDateUtils.get_second()
        print(s1)
        time.sleep(5)
        s2 = XsDateUtils.get_second()
        print(s2)
        s3 = s2 - s1
        print(s3)
        self.assertEqual(5, s3)

    def testGetSpan(self):
        tp = 's'
        date1 = XsDateUtils.get_now()
        date2 = XsDateUtils.add_date(7,target=date1, tp=tp)
        sp = XsDateUtils.get_span(date1,date2,tp=tp)
        print(sp)
        self.assertEqual(7, sp)

    def testIntToStr(self):
        t = XsDateUtils.seconds_to_str()
        print(t)
        t2 = XsDateUtils.seconds_to_day_str()
        print(t2)

    def test_get_time_tuple(self):
        t = XsDateUtils.seconds_to_tuple()
        print(t)

    def test_tuple_to_seconds(self):
        t = XsDateUtils.tuple_to_seconds()
        print(t)

    def test_str_to_tuple(self):
        # t_str = '2021-01-05 12:20:01'

        t_str = XsDateUtils.get_now_str()
        t = XsDateUtils.str_to_tuple(t_str, format_t="%Y-%m-%d %H:%M:%S")
        print(t)