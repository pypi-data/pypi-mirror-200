# -*- coding: utf-8 -*-
"""
 发送邮件,具体使用查看测试示例
"""
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailSender:

    def __init__(self, smtpserver: str, username: str, password: str, is_show_log=False, sender=None):
        """
        构造一个邮件发送实例
        :param smtpserver: smtp 服务器，如 smtp.163.com
        :param username: 邮箱的登录账号，如 abc123@163.com
        :param password: 邮箱的登录密码
        :param is_show_log: 是否打印发送发送过程中交互日志,默认为不打印
        :param sender: 发送人邮箱地址，不填将使用邮箱的登录账号
        """
        __smtp = smtplib.SMTP()
        __smtp.connect(smtpserver)
        if is_show_log:        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
            __smtp.set_debuglevel(1)
        __smtp.login(username, password)
        self.smtp = __smtp
        self.sender = sender if sender else username
        self.msg = MIMEMultipart('mixed')
        self.msg['From'] = '{} <{}>'.format(username, username)

    def add_text(self, text_plain):
        '''
        构造文字内容
        :param text_plain: 字符串文件 可以使用回车换行等符号
        :return:
        '''
        text_plain = MIMEText(text_plain, 'plain', 'utf-8')
        self.msg.attach(text_plain)

    def add_img(self, img_name, img_path):
        """
        添加图片附件
        :param img_name: 图片名称，如abc.png
        :param img_path: 图片的存放路径，可以是相对地址也可以是绝对地址
        :return:
        """
        with open(img_path, 'rb') as fs:
            sendimagefile = fs.read()
            image = MIMEImage(sendimagefile)
            image.add_header('Content-ID', '<image1>')
            image["Content-Disposition"] = 'attachment; filename="{}"'.format(img_name)
            self.msg.attach(image)

    def add_html(self, html):
        '''
        发送html
        :param html: html文件
        :return:
        '''
        text_html = MIMEText(html, 'html', 'utf-8')
        text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        self.msg.attach(text_html)

    def add_file(self, filename, file_path):
        """
        添加文件类型的附件
        :param filename: 文件名称，如 abc.zip
        :param file_path: 文件的存放路径，可以是相对路径也可以是绝对路径
        :return:
        """
        # 构造附件
        with open(file_path, 'rb') as fs:
            sendfile = fs.read()
            text_att = MIMEText(sendfile, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            # 以下附件可以重命名成aaa.txt
            # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
            # 另一种实现方式
            text_att.add_header('Content-Disposition', 'attachment', filename=filename)
            # 以下中文测试不ok
            # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
            self.msg.attach(text_att)

    def send(self, send_to: str, title=None):
        """
        发送一份邮件
        :param send_to: 发送目标地址
        :param title: 邮件标题
        :return:
        """
        subject = title if title else f'系统邮件发送于{datetime.datetime.now()}'
        self.sends([send_to], subject)

    def sends(self,send_to: [str], title=None):
        """
        批量发送邮箱
        :param send_to: 发送目录，是一个字符列表，可存放多个目标地址
        :param title: 邮件标题
        :return:
        """
        subject = title if title else f'系统邮件发送于{datetime.datetime.now()}'
        # 发送邮件
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        self.msg['Subject'] = subject
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        self.msg['To'] = ";".join(send_to)
        self.msg['Date'] = '{}'.format(datetime.datetime.now())
        self.smtp.sendmail(self.sender, send_to, self.msg.as_string())

    def quit(self):
        self.smtp.quit()

