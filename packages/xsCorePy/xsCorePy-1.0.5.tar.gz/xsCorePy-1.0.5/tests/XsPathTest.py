from unittest import TestCase

from XsCore import XsPath


class FileListTest(TestCase):

    def testGetSubFiles(self):
        fs = XsPath.getSubFiles(r"D:\web",['.txt'])
        print(fs)

    def testGetSubFiles2(self):
        fs = XsPath.getSubFiles("images")
        print(fs)
