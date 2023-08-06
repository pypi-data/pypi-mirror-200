"""
自定义异常
"""


class XsException(Exception):
    def __init__(self, err='来自XsCode的异常'):
        Exception.__init__(self, err)
