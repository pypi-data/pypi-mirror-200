from unittest import TestCase

from XsCore import Encrypt


class EncryptTest(TestCase):
    def testmd5EncodeStr(self):
        rz = Encrypt.md5("我是中国人")
        print(rz)

    def testAesEncrypt(self):
        key = "ONxYDyNaCoyTzsp83JoQ3YYuMPHxk3j7"
        vi = "aUaCoyTaut13JoQ9"
        rz = Encrypt.aesEncrypt("我是真正的中国人", key, is_base64=False)
        print(rz)
        self.assertTrue(rz, "D76A63E5A2E354241DA1806740F0B955998B3AAD70E40BF74B35A180A4028AF5")

    def testAesDecrypt(self):
        key = "ONxYDyNaCoyTzsp83JoQ3YYuMPHxk3j7"
        vi = "aUaCoyTaut13JoQ9"
        rz = Encrypt.aesDecrypt("D76A63E5A2E354241DA1806740F0B955998B3AAD70E40BF74B35A180A4028AF5", key,
                                is_base64=False)
        print(rz)
        self.assertTrue(rz, "我是真正的中国人")

    def testRSA_Create_Key(self):
        keys = Encrypt.rsaCreateKey()
        # print("私钥：")
        # print(keys["private"])
        # print("公钥：")
        # print(keys["public"])

        encode = Encrypt.rsaEncryptByPublic("那一天，我来到一条小河边", keys["public"])
        print("加密的数据:")
        print(encode)

        decode = Encrypt.rsaDecryptByPrivate(encode, keys["private"])
        print("解密后:")
        print(decode)

        signData = Encrypt.rsaSignByPrivate(decode, keys["private"])
        print("明文的 签名数据:")
        print(signData)

        isok = Encrypt.rsaCheckSignByPublic(decode, signData, keys["public"])
        if isok:
            print("签名验证正确")
        else:
            print("签名验证错误")
