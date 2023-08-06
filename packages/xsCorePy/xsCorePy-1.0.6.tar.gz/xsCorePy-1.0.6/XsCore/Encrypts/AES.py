import base64

# from Crypto.Cipher import AES
# from crypto.Cipher import AES
from Crypto.Cipher import AES

"""
AES对称加密，本工具主要实现CBC模式加密,特点：
1.支持nopadding与非nopadding
2.支持输出base64或hex
"""

def aesEncryptXs(content=None, key=None, vi='aUaCoyTaut13JoQ9', is_base64=True, nopadding=True):
    """
    # 密钥（key）, 密斯偏移量（iv） CBC模式加密
    :param content:
    :param key:
    :param vi:
    :param is_base64:
    :param nopadding:
    :return:
    """
    length = 16  # 这里只是用于下面取余前面别以为是配置
    count = len(content.encode('utf-8'))  # 这是我上传的主要目的，字符长度不同所以不能直接用，需要先编码转成字节
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0  # 看看你们对接是满16的时候加上16还是0.这里注意
    # 其它语言nopadding时，python还是需要‘’或'x00'这里注意与其它语言对接注
    # 需要使用上面的字符集去填充，如果是真的是 nopadding 的话 这个加的是
    if nopadding:
        text1 = content + '' + (' ' * add)
    else:
        # 字符串补位--最后一位就是位数 需要补充多少位的数据
        consult = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        text1 = content + '' + (consult[add - 1] * add)

    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(text1.encode('utf8'))
    if is_base64:
        return str(base64.b64encode(encryptedbytes), encoding='utf-8')
    else:
        return encryptedbytes.hex().upper()



def aesDecryptXs(content: str, key: str, vi='aUaCoyTaut13JoQ9', is_base64=True, nopadding=True):
    # vi = '5928772605893626'
    # encodebytes = base64.decodebytes(data)

    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    #  # 将加密数据转换位bytes类型数据fromhex
    temp = None
    if is_base64:
        temp = base64.b64decode(content)
    else:
        temp = bytes.fromhex(content.lower())

    text_decrypted = cipher.decrypt(temp)
    # 解密-bytesToString 字节转字符串
    str_text_decrypted = bytes.decode(text_decrypted, encoding='utf8')
    if nopadding:
        return str_text_decrypted.rstrip(' ')
    else:
        consult = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        # 截取最后一位标记- # 字符串补位--最后一位就是位数 需要补充多少位的数据
        num = 0
        # 获取最后一个位数的
        mark_str_index = str_text_decrypted[-1:]
        for i, val in enumerate(consult):
            # 计算出现的位置索引号
            if val == mark_str_index:
                num = int(i) + 1
                break
    return str_text_decrypted[:-num]