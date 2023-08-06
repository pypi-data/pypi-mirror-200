
"""
aes采用pycryptodome库：
pip install pycryptodome
"""
from XsCore.Encrypts import xsMd5, aesEncryptXs, aesDecryptXs,   rsa_create_keys, \
    rsa_encrypt_by_public_key,  rsa_sign_by_private_key, rsa_decrypt_by_private_key, \
    rsa_check_sign_by_public_key


class Encrypt:
    @staticmethod
    def md5(content: str):
        return xsMd5(content)

    # 密钥（key）, 密斯偏移量（iv） CBC模式加密
    @staticmethod
    def aesEncrypt(content=None, key=None, vi='aUaCoyTaut13JoQ9', is_base64=True, nopadding=True):
        return aesEncryptXs(content, key, vi, is_base64, nopadding)


    @staticmethod
    def aesDecrypt(content: str, key: str, vi='aUaCoyTaut13JoQ9', is_base64=True, nopadding=True):
        return aesDecryptXs(content, key, vi, is_base64, nopadding)



    @staticmethod
    def rsaCreateKey():
        return rsa_create_keys()

    @staticmethod
    def rsaEncryptByPublic(message, public_key: bytes):
        """
        使用公钥加密
        :param message:要加密的内容
        :param public_key:公钥
        :return:返回加密结果->bytes,如 b'C+zWS1NFw7sC8...
        """
        return rsa_encrypt_by_public_key(message, public_key)

    @staticmethod
    def rsaDecryptByPrivate(message, private_key: bytes):
        """
        使用私钥解密
        :param message:要解密的内容
        :param private_key:私钥
        :return:返回明文
        """
        return rsa_decrypt_by_private_key(message, private_key)

    @staticmethod
    def rsaSignByPrivate(message, private_key: bytes):
        """
        使用私钥对内容进行签名
        :param message: 要签名的内容
        :param private_key: 私钥
        :return: 返回签名结果->bytes,如 b'dlJ1lLJB60...
        """
        return rsa_sign_by_private_key(message, private_key)

    def rsaCheckSignByPublic(message, signature, public_key: bytes) -> bool:
        """
        使用公钥验证签名数据是否正确
        :param message: 被签名的原文
        :param signature: 签名数据
        :param public_key: 公钥
        :return: 返回是否正确，bool
        """
        return rsa_check_sign_by_public_key(message, signature, public_key)