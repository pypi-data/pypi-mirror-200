import os
from configparser import ConfigParser

"""
操作 ini的工具类
两种实例:
    1.你可以采用 XsIniUtils 来实例化ini对象，构造函数的filename可以是相对路径也可以是绝对路径
        参照测试 testGetAllSections
    2.你可以将你的配置文件放在当前目录下的conf/conf.ini目录下，直接使用xsIni这个单例来操作(推荐)
        参照测试 testDefaultInstance
具体操作请参照测试样例
"""


class XsIniUtils(ConfigParser):
    __default_section = "App"

    def __init__(self, filename):
        """
        构造方法
        :param filename: filename可以是绝对路径或相对路径
        """
        # 调用父类的init方法
        super().__init__()
        # currentPath = os.path.abspath(filename)  # [path, os.path.abspath(path)][isRelative]
        # print(currentPath)  # cfg.ini的路径
        self._filename = filename
        self.read(filename, encoding="utf8")  # python3 如果文件里有中文，需要加上这个encoding

    def getAllSections(self):
        """
        # 获取所有的section
        :return:
        """
        return self.sections()

    def getAppValue(self, keyName: str):
        """
        基于App节点的获取操作
        :param keyName:键名
        :return:返回值字符
        """
        return self.get(self.__default_section, keyName)

    def getAppInt(self, keyName: str):
        """
        基于App节点的获取操作
        :param keyName:键名
        :return:返回值整数
        """
        return self.getint(self.__default_section, keyName)

    def getAppFloat(self, keyName: str):
        """
        基于App节点的获取操作
        :param keyName:键名
        :return:返回浮点
        """
        return self.getfloat(self.__default_section, keyName)

    def getAppBool(self, keyName: str):
        """
        基于App节点的获取操作
        :param keyName:键名
        :return:返回布尔
        """
        return self.getboolean(self.__default_section, keyName)

    def setAppItem(self, key, value):
        """
        基于App节点的更新或添加操作，如果存在key则更新，不存在key则更新
        :param key:键名
        :param value:值
        :return:
        """
        self.set(self.__default_section, key, value)
        with open(self._filename, "w", encoding="utf-8") as fs:
            self.write(fs)


"""
XsIniUtils的默认单例,要求要将配置文件存放在当前目录的conf/conf.ini下
"""
xsIni = XsIniUtils("conf/conf.ini")
