from unittest import TestCase

from XsCore import XsIniUtils, xsIni


class StringUtilsTest(TestCase):

    def testGetAllSections(self):
        """
        演示操作指定目录下的ini文件
        :return:
        """
        cf = XsIniUtils("conf/conf.ini")
        print("siteName:", cf.getAppValue('sitename'))

        cf.setAppItem("sitename3", "binanceusdm,aofex")

    def testDefaultInstance(self):
        """
        这里演示使用默认的实例操作ini,要求一定要将ini文件保存在当前目录下的conf/conf.ini
        :return:
        """
        print("siteName2:", xsIni.getAppValue('sitename2'))
