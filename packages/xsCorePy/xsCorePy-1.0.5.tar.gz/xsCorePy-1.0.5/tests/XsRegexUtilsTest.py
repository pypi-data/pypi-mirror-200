import re
from unittest import TestCase

from XsCore import XsRegexUtils, XsHttp


class FileListTest(TestCase):
    def testFindStrToList(self):
        htmlc = XsHttp.getText('http://www.beimai.com/baike/243a107743b0c.html')

        rzs = XsRegexUtils.FindStrToList(
            r'(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)', htmlc)
        for url in rzs:
            print(url)

    def testFindStrToList(self):
        htmlc = XsHttp.getText('http://www.beimai.com/baike/243a107743b0c.html')

        rzs = XsRegexUtils.FindStrToList(r'[\u4e00-\u9fa5]+', htmlc)
        for url in rzs:
            print(url)

    def testFindOne(self):
        testTxt = 'Cats are aaa smarter than bbb dogs'

        rzs = XsRegexUtils.FindOne(r'(?<=(aaa))[.\s\S]*?(?=(bbb))', testTxt)

        print("结果：", rzs)

    def testReplaceAll(self):
        phone = "2004-959-559 # 这是一个国外电话号码<image src='https://www.runoob.com/python/python-reg-expressions.html' />"

        rzs = XsRegexUtils.ReplaceAll(r'[<].*?[>]', phone, "")
        print(rzs)

    def testReplaceCustom(self):
        testTxt = 'A23G4HFD567'
        rzs = XsRegexUtils.ReplaceCustom(r'(?P<value>\d+)', testTxt, self.__customReplace)
        print(rzs)

    def __customReplace(self, matched):
        value = int(matched.group('value'))
        return str(value * 2)

    def testIsMatch(self):
        isHave = XsRegexUtils.IsMatch(r"\d{15}|\d{18}", "44082419800918186655588444")
        self.assertTrue(isHave, True)
