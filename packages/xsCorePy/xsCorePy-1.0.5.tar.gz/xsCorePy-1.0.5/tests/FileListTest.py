from unittest import TestCase

from XsCore.XsFso.FileList import XsFileList


class FileListTest(TestCase):

    def testSubList(self):

        # xsFl = XsFileList("D:\work\管理\CoinBig", ['.txt'])
        xsFl = XsFileList("images", ['.txt'])
        lsRz = xsFl.getSubFiles()
        for sP in lsRz:
            print(sP)
        self.assertTrue(len(lsRz) > 1)

    def testSubListAsync(self):
        '''
        异步调用
        :return:
        '''
        xsFl = XsFileList("D:\work\管理\CoinBig")
        xsFl.getSubFilesAsync(self.callBackFile)  # 类似C#的委托

    def callBackFile(self, src):
        print(src)

