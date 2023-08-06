import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from XsCore.XsException import XsException


class XsPool:
    def __init__(self, max_task=10,is_future=False, is_process=False):
        """
        构造一个线程或进程池实例
        :param max_task: 最大并发数
        :param is_future: 是否获取任务的使用情况
        :param is_process: 是否进程池，默认为线程池，线程池只能使用一个cpu，如果为True，将使用进程池
        """
        self.executor = ProcessPoolExecutor(max_workers=max_task) if is_process else ThreadPoolExecutor(max_workers=max_task)
        self.tasks = []
        self.isfuture = is_future

    def addTask(self, fn, /, *args, **kwargs):
        """
        添加一个任务到池子
        :param fn: 任务，方法或者说是函数
        :param args: 函数的参数，或多个
        :param kwargs: 函数的参数，或多个，关键字的方式
        :return:
        """
        # future列表中每个future完成的顺序，和它在列表中的顺序并不一定完全一致。
        # 到底哪个先完成、哪个后完成，取决于系统的调度和每个future的执行时间

        future = self.executor.submit(fn, *args, **kwargs)
        if self.isfuture:
            self.tasks.append(future)

    def __clearDone(self):
        """
        清理已经完成的任务
        :return:
        """
        rmTem = []
        for task in self.tasks:
            if task.done():  # done()返回True表示任务成功取消或者完成
                rmTem.append(task)
        for tp in rmTem:
            self.tasks.remove(tp)

    def getWaitingCount(self):
        """
        获取等待中的任务数
        :return:
        """
        if self.isfuture:
            self.__clearDone()
            return len(self.tasks)
        else:
            raise XsException(err="要调用此方法，请在构造的时候指定is_future为True")

    def getRunningCount(self):
        """
        获取执行中的任务数
        :return:
        """
        if self.isfuture:
            _count = 0
            for task in self.tasks:
                if task.running():
                    _count += 1
            return _count
        else:
            raise XsException(err="要调用此方法，请在构造的时候指定is_future为True")


    def shutdown(self):
        self.executor.shutdown()
