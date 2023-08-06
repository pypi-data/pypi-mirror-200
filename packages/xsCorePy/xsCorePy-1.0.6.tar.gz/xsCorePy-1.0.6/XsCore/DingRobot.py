import json

import requests

"""
钉钉地群机器人消息发送
"""


class DingRobot:
    @staticmethod
    def send(access_token: str, msg: str, is_at_all=True):
        """
        发送群消息
        :param access_token: 申请到的机器人token
        :param msg: 要发送的消息,注:必须的你设置在机器人里的关键字，如配置有关键字【行情】，可以这样编写【行情提醒: BTC: 流通市值：6.97万亿 价格：37.01万】
        :param is_at_all: 是否@所有人
        :return:
        """
        # 发起POST请求时，必须将字符集编码设置成UTF - 8。
        # 每个机器人每分钟最多发送20条。消息发送太频繁会严重影响群成员的使用体验，大量发消息的场景(譬如系统监控报警)
        # 可以将这些信息进行整合，通过markdown消息以摘要的形式发送到群里。
        # 请求的URL，WebHook地址
        webhook = f"https://api.dingtalk.com/robot/send?access_token={access_token}"
        # 构建请求头部
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        # 构建请求数据
        message = {

            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {

                "isAtAll": is_at_all
            }

        }
        # 对请求的数据进行json封装
        message_json = json.dumps(message)
        # 发送请求
        info = requests.post(url=webhook, data=message_json, headers=header)
        # 打印返回的结果
        return info.text
