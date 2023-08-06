'''
RSA 非对称加密:
加密的 内容 最大长度是 证书key位数/8 - 11
1024 bit的证书，被加密的最长 1024/8 - 11=117
2048 bit的证书，被加密的最长 2048/8 - 11 =245
RSA 非对称加密主要实现以下4个功能:
1.公钥加密
2.私钥解密
3.私钥签名
4.公钥验签
'''
import base64

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

encode_gbk_utf8 = 'utf-8'  # 全局编码方式 utf-8 | gbk
key_num = 1024  # 证书key位数


def rsa_create_keys() -> {}:
    """
    RSA秘钥对的生成
    :return: 以字典的方式，返回私钥与公钥
    """
    random_generator = Random.new().read  # 伪随机数生成器
    rsa = RSA.generate(key_num, random_generator)  # rsa算法生成实例
    # 秘钥对的生成
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return {"private": private_pem, "public": public_pem}


def rsa_encrypt_by_public_key(message, public_key: bytes):
    """
    使用公钥加密
    :param message:要加密的内容
    :param public_key:公钥
    :return:返回加密结果->bytes,如 b'C+zWS1NFw7sC8...
    """
    rsakey = RSA.importKey(public_key)  # 导入读取到的公钥
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    # 加密message明文，python3加密的数据必须是bytes，不能是str
    cipher_text = base64.b64encode(cipher.encrypt(
        message.encode(encoding=encode_gbk_utf8)))
    return cipher_text


def rsa_decrypt_by_private_key(message, private_key: bytes):
    """
    使用私钥解密
    :param message:要解密的内容
    :param private_key:私钥
    :return:返回明文
    """
    rsakey = RSA.importKey(private_key)  # 导入读取到的私钥
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    # 将密文解密成明文，返回的是bytes类型，需要自己转成str,主要是对中文的处理
    text = cipher.decrypt(base64.b64decode(message), "ERROR")
    return text.decode(encoding=encode_gbk_utf8)


def rsa_sign_by_private_key(message, private_key: bytes):
    """
    使用私钥对内容进行签名
    :param message: 要签名的内容
    :param private_key: 私钥
    :return: 返回签名结果->bytes,如 b'dlJ1lLJB60...
    """
    rsakey = RSA.importKey(private_key)
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode(encoding=encode_gbk_utf8))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)  # 对结果进行base64编码
    return signature


def rsa_check_sign_by_public_key(message, signature, public_key: bytes) -> bool:
    """
    使用公钥验证签名数据是否正确
    :param message: 被签名的原文
    :param signature: 签名数据
    :param public_key: 公钥
    :return: 返回是否正确，bool
    """
    rsakey = RSA.importKey(public_key)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    # 注意内容编码和base64解码问题
    digest.update(message.encode(encoding=encode_gbk_utf8))
    is_verify = verifier.verify(digest, base64.b64decode(signature))
    return is_verify
