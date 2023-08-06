from typing import Any

from XsCore import XsRegexUtils


class XsStrings:

    @staticmethod
    def clearHtml(html):
        """
        将内容里的html标签清除
        :param html:带有html标签的内容
        :return:
        """
        rz = XsRegexUtils.ReplaceAll(r'[<].*?[>]', html)
        return rz

    @staticmethod
    def cutStartEndList(txt: str, start: str, end: str) -> list[str]:
        """
        指定起始字符，截取中间的字符，将所有匹配到的字符并返回一个列表
        :param txt:要截取的内容
        :param start:开始标记
        :param end: 结束标记
        :return: 返回列表
        """
        rz = XsRegexUtils.FindStrToList(r'(?<=(' + start + '))[.\s\S]*?(?=(' + end + '))', txt)
        return rz

    @staticmethod
    def cutStartEndFirst(txt: str, start: str, end: str) -> str:
        """
        指定起始字符，截取中间的字符，返回第一个
        :param txt:要截取的内容
        :param start:开始标记
        :param end:结束标记
        :return: 返回第一个匹配到的字符
        """
        rz = XsRegexUtils.FindOne(r'(?<=(' + start + '))[.\s\S]*?(?=(' + end + '))', txt)
        return rz

    @staticmethod
    def splitLines(txt: str) -> list[str]:
        """
        将字符分割成列表,分割符为各种换行包括回车
        :param txt: 要分割的字符
        :return:
        """
        return txt.splitlines()

    @staticmethod
    def split(txt: str, strSplit: str = ',') -> list[str]:
        """
        将字符分割成列表,默认以,号分割，可以自定义分割符号
        :param txt: 要分割的字符
        :param strSplit: 分割符号
        :return:
        """
        return txt.split(strSplit)

    @staticmethod
    def getChinese(txt) -> list[str]:
        """
        提取内容中的中文
        :param txt: 内容
        :return:
        """
        rzs = XsRegexUtils.FindStrToList(r'[\u4e00-\u9fa5]+', txt)
        return rzs

    @staticmethod
    def getHtmlUrls(html: str) -> list[str]:
        """
        提取html中的网址，包括非a标签内容
        :param html:
        :return:
        """
        rzs = XsRegexUtils.FindStrToList(
            r'(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)', html)
        return rzs




