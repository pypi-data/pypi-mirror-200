from unittest import TestCase

from XsCore import EmailSender

smtpServer = 'smtp.163.com'
userName = 'xxx@163.com'
passWord = 'xxxxxx'

class EmailSenderTest(TestCase):

    def testSendEmailText(self):
        em_obj = EmailSender(smtpServer, userName, passWord)
        em_obj.add_text('这是发送到qq邮箱的测试邮件发送代码，无需回复')
        em_obj.send('xxx@qq.com')
        em_obj.add_text('这是发送到gmail测试邮件发送代码，无需回复')
        em_obj.sends(['xxx@gmail.com'])
        em_obj.quit()
        print("发送成功")

    def testSendEmailImage(self):
        em_obj = EmailSender(smtpServer, userName, passWord)
        em_obj.add_text('随带图片测试邮件，无需回复')
        em_obj.add_img("baidulogo.png", 'images/baidulogo.png')
        em_obj.send('xxx@qq.com')
        em_obj.quit()
        print("发送成功")

    def testSendEmailFile(self):
        em_obj = EmailSender(smtpServer, userName, passWord)
        em_obj.add_text('随带文件的测试邮件，无需回复')
        em_obj.add_file("testddd.zip", 'images/testddd.zip')
        em_obj.send('xxx@qq.com')
        em_obj.quit()
        print("发送成功")