import logging
from logging.handlers import RotatingFileHandler

from XsCore.XsFso import XsPath


class Logger:
    def __init__(self, path, log_count=100, max_mb=1, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        """
        创建一个日志操作实例
        :param path: 日志的路径，可以是相对路径，也可以是绝对路径
        :param log_count: 最多保留几个日志文件，默认最多保留100个日志文件
        :param max_mb:  一个日志文件最大保存多少MB
        :param cmd_level: 终端输出的日志级别
        :param file_level:  文件输出日志级别
        """

        # # <editor-fold desc="判断日志文件的目录是否存在，如果不存在就创建一个">
        if not XsPath.isFullPath(path):
            path = XsPath.getFullPath(path)

        XsPath.exists(path, isMake=True)
        # </editor-fold>

        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        self.logger.addHandler(sh)

        # 设置文件日志
        # maxBytes = 1 * 1024 * 1024
        file_hd = RotatingFileHandler(filename=path, maxBytes=max_mb * 1024 * 1024, backupCount=log_count,
                                      encoding='utf-8')
        file_hd.setFormatter(fmt)
        file_hd.setLevel(file_level)
        self.logger.addHandler(file_hd)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


