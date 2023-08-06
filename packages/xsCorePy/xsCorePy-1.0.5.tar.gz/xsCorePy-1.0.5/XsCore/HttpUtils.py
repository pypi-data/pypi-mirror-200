import json
import urllib

import requests


class XsHttp:

    @staticmethod
    def request(url: str, method: str, param=None, headers=None, is_json=True, content_type: str = None, time_out=None, cookie=None ):
        """
        一个通用的http请求方法，目前只支持get与post,后期会更新
        :param cookie: cookies 采用字典保存
        :param url: 请求的地址
        :param method: 请求的方法
        :param param:   请求参数，一个字典对象
        :param headers: 请求头，一个字典对象
        :param is_json: 返回的结果是否转换成json对象
        :param content_type: 请求时的Content-type类型，比如application/json
        :param time_out: 超时
        :return: 返回文本或json
        """
        try:
            if method == 'get':
                r = requests.get(url=url, params=param, headers=headers, timeout=time_out, cookies=cookie)
                r.encoding = r.apparent_encoding  # 服务器传过来的编码格式需要 先转换一下，再转成json格式 否则json格式的数据存在乱码
                result = r.json() if is_json else r.text  # 相当于问题表达式，意思是如果is_json不真，result=r.json()否则result = r.text
                return result
            elif method == 'post':
                if content_type == 'application/json':
                    headers['Content-type'] = "application/json;charset=UTF-8"
                    r = requests.post(url=url, json=param, headers=headers, timeout=time_out, cookies=cookie)
                    r.encoding = r.apparent_encoding
                    result = r.json() if is_json else r.text
                    return result
                else:
                    r = requests.post(url=url, data=param, headers=headers, timeout=time_out, cookies=cookie)
                    r.encoding = r.apparent_encoding
                    result = r.json() if is_json else r.text
                    return result
            else:
                print("http method not allowed")
        except Exception as e:
            print("http请求报错:{0}".format(e))

    @staticmethod
    def getText(url: str, params_obj={}, headers={}) -> str:
        """
        使用get方式请求地址
        :param url: 请求地址
        :param params_obj: 请求头，一个字典对象
        :param headers: 请求参数，一个字典对象
        :return: 返回文本
        """
        return XsHttp.request(url, "get", params_obj, headers, False)

    @staticmethod
    def getJson(url: str, params_obj={}, headers={}) -> str:
        """
        使用get方式请求地址
        :param url: 请求地址
        :param params_obj: 请求参数，一个字典对象
        :param headers:  请求头，一个字典对象
        :return: 返回字典类型JSON对象
        """
        return XsHttp.request(url, "get", params_obj, headers, True)

    @staticmethod
    def postText(url: str, params_obj={}, headers={}):
        """
        使用post方式请求地址
        :param url: 请求地址
        :param params_obj: 请求参数，一个字典对象
        :param headers: 请求头，一个字典对象
        :return: 返回文本
        """
        return XsHttp.request(url, "post", params_obj, headers, False)

    @staticmethod
    def postJson(url: str, params_obj={}, headers={}):
        """
        使用post方式请求地址
        :param url: 请求地址
        :param params_obj: 请求参数，一个字典对象
        :param headers: 请求头，一个字典对象
        :return: 返回字典类型JSON对象
        """
        return XsHttp.request(url, "post", params_obj, headers, True)

    @staticmethod
    def postJsonContent(url: str, content_obj={}, headers={}):
        """
        使用post方式请求地址,请求提交的内容为json
        :param url: 请求地址
        :param content_obj: 请求参数，一个字典对象
        :param headers: 请求头，一个字典对象
        :return: 返回字典类型JSON对象
        """
        return XsHttp.request(url, "post", content_obj, headers, True, "application/json")

    @staticmethod
    def postHttpContent(url: str, content_obj={}):
        """
        使用post方式请求地址,将一个对象以HttpContent的方式提交
        :param url: 请求地址
        :param content_obj:
        :param headers: 请求头，一个字典对象
        :return: 返回字典类型JSON对象
        """
        headers = {'Content-Type': 'text/plain'}
        return XsHttp.request(url, "post", content_obj, headers, True)