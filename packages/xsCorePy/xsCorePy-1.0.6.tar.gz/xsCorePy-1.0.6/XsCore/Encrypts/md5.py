import hashlib


def xsMd5(content: str):
    return hashlib.new('md5', content.encode()).hexdigest()