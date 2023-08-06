from unittest import TestCase

from XsCore import XsHttp


class XsHttpTest(TestCase):

    def testGetText(self):
        rz = XsHttp.getText("https://www.baidu.com")
        print(rz)
        self.assertTrue(1, 1)

    def testGetJson(self):
        prams = {"symbol": "BTC-SWAP-USDT"}
        rz = XsHttp.getJson("https://api.coinbigcn.top/openapi/contract/v1/fundingRate", prams)
        print(rz)
        self.assertTrue(1, 1)

    def testGetJson2(self):
        rz = XsHttp.getJson("https://api.coinbigcn.top/openapi/contract/v1/fundingRate")
        for item in rz:
            print(item["symbol"])
        self.assertTrue(1, 1)
