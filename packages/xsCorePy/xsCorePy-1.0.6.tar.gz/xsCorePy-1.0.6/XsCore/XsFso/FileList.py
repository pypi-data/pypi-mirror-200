import threading

from XsCore.XsFso import XsPath


class XsFileList:
    def __init__(self, path, extension: [str] = []):
        self.__fun = None
        self._path = path
        self._extension: [str] = extension
        self._files = []

    def getSubFiles(self):
        self.__fun = None
        self.__scanFiles(self._path)
        return self._files

    def getSubFilesAsync(self, callBack):
        self.__fun = callBack
        thr = threading.Thread(target=self.__startScan)  # , args=(self._path,)
        thr.start()

    def __startScan(self):
        self.__scanFiles(self._path)
        if self.__fun is not None:
            self.__fun("--end--")

    def __scanFiles(self, parentPath):
        # time.sleep(1)
        temps = XsPath.getSubFileOrDirs(parentPath)
        for tp in temps:
            child = XsPath.joinPath(parentPath, tp)
            if XsPath.isDir(child):
                self.__scanFiles(child)
            else:
                if len(self._extension) > 0:
                    if child[-4:] in self._extension:
                        if self.__fun is not None:
                            self.__fun(child)
                        else:
                            self._files.append(child)
                else:
                    if self.__fun is not None:
                        self.__fun(child)
                    else:
                        self._files.append(child)
