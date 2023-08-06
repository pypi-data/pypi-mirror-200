import os


class XsPath:


    @staticmethod
    def joinPath(path, *paths):
        return os.path.join(path, *paths)

    @staticmethod
    def getSubFileOrDirs(src: str) -> list[str]:
        """
        获取一个目录下的子目录与文件列表
        :param src:父目录
        :return:保存了目录与目录路径的列表
        """
        return os.listdir(src)

    @staticmethod
    def getDirPath(src):
        """
        获取文件路径中的目录路径，也就是将文件名去除,只保留目录路径
        :param src: 文件路径
        :return:
        """
        return os.path.dirname(src)

    @staticmethod
    def getSubDirs(src: str) -> list[str]:
        """
        获取一个目录下的所有子目录
        :param src: 父目录
        :return: 保存了目录的列表
        """
        rzDirs: list[str] = []
        temps: list[str] = os.listdir(src)
        for tp in temps:
            child = os.path.join(src, tp)
            if os.path.isdir(child):
                rzDirs.append(child)
        return rzDirs

    @staticmethod
    def getSubFiles(src: str, extension: [str] = []):
        """
        获取一个目录下的所有文件，默认没有筛选条件
        :param src: 目录路径
        :param extension: 筛选条件 如: ['.txt','.pdf']
        :return: 返回文件路径的列表
        """
        rzFiles: list[str] = []
        temps: list[str] = os.listdir(src)
        for tp in temps:
            child = os.path.join(src, tp)
            if os.path.isfile(child):
                if len(extension) > 0:
                    if child[-4:] in extension:
                        rzFiles.append(child)
                else:
                    rzFiles.append(child)

        return rzFiles

    @staticmethod
    def getFullPath(src: str) -> str:
        """
        获取文件的绝对路径
        :param src: 相对路径
        :return:
        """
        return os.path.abspath(src)  # 'test.csv'

    @staticmethod
    def isFullPath(src: str) -> bool:
        """
        检查目录是否绝对路径
        :param src: 需要检查的目录
        :return:
        """
        return os.path.isabs(src)

    @staticmethod
    def isFile(src: str) -> bool:
        """
        检测路径是否文件
        :param src: 需要检查的路径
        :return:文件返回true,目录返回false
        """
        return os.path.isfile(src)

    @staticmethod
    def isDir(src: str) -> bool:
        return os.path.isdir(src)

    @staticmethod
    def exists(src: str, isMake=False) -> bool:
        """
        检查路径是否存在
        :param isMake:是否在不存在的情况下生成一个文件假
        :param src:
        :return:
        """
        isHave = os.path.exists(src)
        if not isHave and isMake:
            if not XsPath.isDir(src):
                src = XsPath.getDirPath(src)
            os.makedirs(src)
        return isHave

    @staticmethod
    def mkdir(src):
        """判断文件夹是否存在，不存在就创建"""
        if not os.path.exists(src):
            os.makedirs(src)

    @staticmethod
    def normpath(src: str) -> str:
        """
        规范路径
        :param src:
        :return:
        """
        return os.path.normpath(src)

    @staticmethod
    def getModifyTime(src: str):
        """
        获取目录或文件的修改时间
        :param src:
        :return:
        """
        return os.path.getmtime(src)
