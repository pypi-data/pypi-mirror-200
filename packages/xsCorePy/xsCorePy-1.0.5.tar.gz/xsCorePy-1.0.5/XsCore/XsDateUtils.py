import datetime
import time

"""
时间日期的相关处理
"""


class XsDateUtils:

    # 获取距离现在时间的任意时间的日期     正数 加,负数 减  return:2019-05-12
    # @staticmethod
    # def getAnyDateTime(day, hour=0, min=0, sec=0):
    #     """
    #          description:  获取距离现在时间的任意时间的日期&时间
    #          day:          天数 1代表当前时间+1天    -1代表当前时间-1天
    #          hour:         小时 2代表当前时间+2h     -2代表当前时间-2h     默认=0
    #          min:          分钟 30代表当前时间+30min -30代表当前时间-30m   默认=0
    #          sec:          秒   120代表当前时间+120s -120代表当前时间-120s 默认=0
    #          return:       2019-05-15 15:37:41 -> str
    #          """
    #
    #     return \
    #         str(datetime.datetime.now() + datetime.timedelta(days=day, hours=hour, minutes=min, seconds=sec)).split(
    #             ".")[0]

    # @staticmethod
    # def getAnyDateSecondTime(day, hour=0, min=0, sec=0):
    #     """
    #          description:  获取距离现在时间的任意时间的秒数
    #          day:          天数 1代表当前时间+1天    -1代表当前时间-1天
    #          hour:         小时 2代表当前时间+2h     -2代表当前时间-2h     默认=0
    #          min:          分钟 30代表当前时间+30min -30代表当前时间-30m   默认=0
    #          sec:          秒   120代表当前时间+120s -120代表当前时间-120s 默认=0
    #          return:       1557902182 -> str
    #          """
    #
    #     anyDay = datetime.datetime.now() + datetime.timedelta(days=day, hours=hour, minutes=min, seconds=sec)
    #     return str(round(time.mktime(anyDay.timetuple())))

    # @staticmethod
    # def getTodayTime():
    #     """
    #          description:  获取当天0点的时间戳
    #          return:       1557676800 -> str
    #          """
    #
    #     return str(round(time.mktime(datetime.date.today().timetuple())))
    #
    # @staticmethod
    # def getCurrentWeekTime():
    #     """
    #          description:  获取本周周一0点
    #          return:       1557676800 -> str
    #          tips:         可替换成: timestamps = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(times)), "%Y-%m-%d"))
    #          """
    #
    #     week = int(time.strftime("%w", time.localtime()))
    #     times = round(time.time()) - (week - 1) * 86400
    #     timestamps = time.mktime(datetime.date.fromtimestamp(times).timetuple())
    #     return str(round(timestamps))

    # @staticmethod
    # def getCurrentTimeStr():
    #     """
    #           description:  获取当前时间的可读形式字符串
    #           return:       Mon May 13 11:27:42 2019 -> str
    #           """
    #
    #     return time.ctime()

    # @staticmethod
    # def getCurrentTimeStrByTuple(tupleTime=time.localtime()):
    #     """
    #           description:  获取指定时间的可读形式字符串
    #           tupleTime:    时间元组 可通过time.localtime() or datetime.datetime.now().timetuple()获取 默认当前时间的元组
    #           return:       Mon May 13 11:27:42 2019 -> str
    #           """
    #
    #     return time.asctime(tupleTime)



    @staticmethod
    def get_milli_second(times=None):
        """
        获取指定时间的时间戳-毫秒级
        :param times: 指定时间，默认为当前时间
        :return: 1639728906765 - int
        """
        if not times:
            times = time.time()
        timestamps = round(times * 1000)
        return timestamps

    @staticmethod
    def get_second(times=None):
        """
        获取指定时间的时间戳-秒级
        :param times:指定时间，默认为当前时间
        :return: 1557730377 -> int
        """
        if not times:
            times = time.time()
        timestamps = round(times)
        return timestamps



    @staticmethod
    def add_date(day_num, target=None, tp='d'):
        """
        给定日期，延长或减少指定时间（天数,小时，分钟，秒)
        :param tp: 类型,d代表天，h代表小时，m代表分钟，s代表秒，默认为d
        :param day_num: 指定天数，可以是负数
        :param target: 指定日期，默认为当天
        :return:
        """
        if not target:
            target = datetime.datetime.now()
        if tp == 'd':
            target += datetime.timedelta(days=day_num)
        elif tp == 'h':
            target += datetime.timedelta(hours=day_num)
        elif tp == 'm':
            target += datetime.timedelta(minutes=day_num)
        elif tp == 's':
            target += datetime.timedelta(seconds=day_num)

        return target

    @staticmethod
    def add_days(day_num, target=None):
        return XsDateUtils.add_date(day_num, target, 'd')

    @staticmethod
    def add_hours(day_num, target=None):
        return XsDateUtils.add_date(day_num, target, 's')

    @staticmethod
    def add_minutes(day_num, target=None):
        return XsDateUtils.add_date(day_num, target, 'm')

    @staticmethod
    def get_span(start, end, tp='d'):
        """
        返回两个时间的时间隔
        :param start: 开始时间
        :param end: 结束时间
        :param tp: 类型，d为天数，s为秒数，mic为毫秒数
        :return:
        """
        span = 0
        if tp == 'd':
            span = (end - start).days
        elif tp == 's':
            span = (end - start).seconds
        elif tp == 'mic':
            span = (end - start).microseconds
        return span

    @staticmethod
    def get_span_days(start, end):
        return XsDateUtils.get_span(start, end, tp='d')

    @staticmethod
    def get_span_seconds(start, end):
        return XsDateUtils.get_span(start, end, tp='s')

    @staticmethod
    def get_now():
        """
        获取当前日期及时间点
        :return:
        """
        return datetime.datetime.now()

    @staticmethod
    def seconds_to_str(times=None, format_t="%Y-%m-%d %H:%M:%S"):
        """
              description:  将指定时间戳转换成可视式时间
              times:        指定时间戳，秒级
              return:       2019-05-13 15:00:47 -> str
              tips:         %y 两位数的年份表示（00-99）    %Y 四位数的年份表示（000-9999）   %m 月份（01-12）    %d 月内中的一天（0-31）
                            %H 24小时制小时数（0-23）      %I 12小时制小时数（01-12）        %M 分钟数（00=59）  %S 秒（00-59）   %w 星期（0-6）
         """
        if not times:
            times = time.time()
        timestamps = time.strftime(format_t, time.localtime(times))
        return timestamps

    @staticmethod
    def seconds_to_day_str(times=None):
        """
        将时间戳转换成天的字符串，不包括时间
        :param times:秒 默认当前时间
        :return: return:       2019-05-13 -> str  一天86400秒
        """
        if not times:
            times = time.time()
        timestamps = str(datetime.date.fromtimestamp(round(times)))
        return timestamps

    @staticmethod
    def seconds_to_tuple(times=None):
        """
        将指定时间戳转换成时间元祖
        :param times: 默认当前时间 可传second
        :return: (tm_year=2019, tm_mon=5, tm_mday=13, tm_hour=10, tm_min=9, tm_sec=18, tm_wday=0, tm_yday=133, tm_isdst=0) -> tuple
        """

        if not times:
            times = time.time()
        timestamps = time.localtime(times)
        return timestamps



    @staticmethod
    def tuple_to_seconds(tupleTime=None):
        """
        将指定的时间元祖转换成时间戳
        :param tupleTime:  默认当前时间的元组 可通过time.localtime() or datetime.datetime.now().timetuple()获取
        :return: 1557733061 -> str
        """
        if not tupleTime:
            tupleTime = time.localtime()
        timestamps = str(round(time.mktime(tupleTime)))
        return timestamps

    @staticmethod
    def str_to_tuple(time_str=None,format_t="%Y-%m-%d %H:%M:%S"):
        """
        将时间字符串转换成时间元祖
        :param time_str: 格式化字符串   如:2019-05-13 15:00:47    默认当前时间
        :param format_t: 格式化规则    如:%Y-%m-%d %H:%M:%S      默认%Y-%m-%d %H:%M:%S
        :return: (tm_year=2019, tm_mon=5, tm_mday=13, tm_hour=10, tm_min=9, tm_sec=18, tm_wday=0, tm_yday=133, tm_isdst=0) -> tuple
        """
        if not time_str:
            time_str = str(datetime.datetime.now()).split(".")[0]
        return time.strptime(time_str, format_t)

    @staticmethod
    def get_now_str():
        """
        获取当前时间日期的字符串
        :return: 2019-05-13 14:41:15 -> str
        """
        timestamps = str(datetime.datetime.now()).split(".")[0]
        return timestamps

    @staticmethod
    def get_today_str():
        """
        获取当天的字符串格式
        :return: 2019-05-13 -> str  与 datetime.datetime.now().date()有相同效果
        """

        timestamps = str(datetime.date.today())
        return timestamps

    @staticmethod
    def get_time_to_str():
        """
        获取当前时间的字符串格式
        :return: 14:41:15 -> str
        """
        timestamps = str(datetime.datetime.now().time()).split(".")[0]
        return timestamps

