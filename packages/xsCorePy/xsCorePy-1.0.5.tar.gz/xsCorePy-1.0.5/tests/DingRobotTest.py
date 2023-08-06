from unittest import TestCase

from XsCore import DingRobot


class DingRobotTest(TestCase):
    def testSend(self):
        # 比如机器人的关键字有【行情】,可以这样编写
        rz = DingRobot.send("c62c46dc6a62985bf42b383763a88e7b0355ebbcfd3ee9d42199d9cef72afd89", "【行情提醒】: BTC: 流通市值：6.97万亿 价格：37.01万")
        print(rz)