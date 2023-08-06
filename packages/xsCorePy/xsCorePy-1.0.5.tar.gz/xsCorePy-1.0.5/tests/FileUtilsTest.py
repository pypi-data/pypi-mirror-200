from unittest import TestCase

from XsCore import XsFso
from XsCore.XsFso.FileList import XsFileList


class FileListTest(TestCase):

    def testReadCode(self):
        content = XsFso.getFileCode(r"D:\web\testddd.txt")
        print(content)

    def testReadAny(self):
        content = XsFso.readFileAnyCode(r"D:\web\testddd.txt")
        print(content)

    def testWriteAny(self):
        XsFso.writeFileAnyCode(r"D:\web\testddd.txt", "ffffffffff举例：有一个data.txt文件，我们不知道它的编码格式，现在我们需要读取文件的编码格式：fff")
