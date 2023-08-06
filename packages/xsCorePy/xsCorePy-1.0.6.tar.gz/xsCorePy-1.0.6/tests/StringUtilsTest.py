from unittest import TestCase

from XsCore import XsHttp, XsStrings


class StringUtilsTest(TestCase):

    def testGetHtmlUrls(self):
        htmlc = XsHttp.getHtml('http://www.beimai.com/baike/243a107743b0c.html')
        urls = XsStrings.getHtmlUrls(htmlc)
        for url in urls:
            print(url)

    def testGetChinese(self):
        cns = XsStrings.getChinese("fsfs我是，opopl中国人")
        for cn in cns:
            print(cn)

    def testSplitLines(self):
        rzs = XsStrings.splitLines("ab c\n\nde fg\rkl\r\n")
        print(rzs)

    def testSplit(self):
        rzs = XsStrings.split("ab cnkde fgnkl",",")
        print(rzs)

    def testCutStartEnd(self):
        testTxt = 'Cats are aaa smarter than bbb dogs'
        rz = XsStrings.cutStartEnd(testTxt, "aaa", "bbb")
        print(rz)