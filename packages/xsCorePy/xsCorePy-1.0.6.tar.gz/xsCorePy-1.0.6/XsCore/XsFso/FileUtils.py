#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件操作类

import os
import logging
import shutil
import zipfile
import chardet


def is_exists_file(src: str):
    return os.path.isfile(src)


def is_exists_folder(dir_path: str):
    return os.path.exists(dir_path)


def getFileCode(src):
    """
    读取文件的编码
    :param src: 文件路径
    :return: 编码格式
    """
    with open(src, "rb") as fr:  # 先用二进制打开
        data = fr.read()  # 读取文件内容
        return chardet.detect(data).get('encoding')  # 得到文件的编码格式


def readFileAnyCode(src) -> str:
    """
    使用当前这个文件的编码来读取这个文件，所以不用指定编码
    :param src: 文件路径
    :return: 内容
    """
    file_encoding = getFileCode(src)
    return readFile(src, file_encoding)


def readFile(src, enc="utf-8") -> str:
    '''
    读取文件
    :param src:
    :param enc:
    :return:
    '''
    with open(src, "r", encoding=enc) as fr:
        file_content = fr.read()  # data 是读取到的结果
    return file_content


def writeFileAnyCode(src, file_content: str) -> bool:
    """
    使用当前这个文件的编码来写文件，所以不用考虑文件编码
    :param src:文件路径
    :param file_content:内容
    :return:是否成功
    """
    file_encoding = getFileCode(src)
    return writeFile(src, file_content, file_encoding)


def writeFile(src, file_content: str, enc="utf-8") -> bool:
    try:
        with open(src, "w", encoding=enc) as fw:
            fw.write(file_content)
        return True
    except Exception as err:
        logging.error(f"出错了:{err}")
        return False


def getFileSize(src):
    """ 文件大小
        Parameters
        ----------
        src : 源路径
    """
    try:
        size = os.path.getsize(src)
        return formatSize(size)
    except Exception as err:
        logging.error(err)


def getFolderSize(src):
    """ 文件夹大小
        Parameters
        ----------
        src : 文件路径
    """
    sumsize = 0
    try:
        filename = os.walk(src)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(src + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        logging.error(err)


def formatSize(bytes):
    """ 格式化文件大小
        Parameters
        ----------
        bytes : 字节大小
    """
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        logging.error("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


def getFileExtension(src):
    """ 获取文件后缀名
        Parameters
        ----------
        src : 文件路径
    """
    return os.path.splitext(src)[1]


def getFileName(src):
    """ 获取文件名
        Parameters
        ----------
        src : 文件路径
    """
    return os.path.basename(src)


def move(src, dest):
    """ 移动
        Parameters
        ----------
        src  : 文件路径
        dest : 目标路径
    """
    if not os.path.isfile(src):
        logging.error("%s not exist!" % (src))
    else:
        fpath, fname = os.path.split(dest)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(src, dest)
        logging.debug("move %s -> %s" % (src, dest))


def copy(src, dest):
    """ 复制
        Parameters
        ----------
        src  : 文件路径
        dest : 目标路径
    """
    if not os.path.isfile(src):
        logging.error("%s not exist!" % (src))
    else:
        fpath, fname = os.path.split(dest)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(src, dest)
        logging.debug("copy %s -> %s" % (src, dest))


def rename(src, dest):
    """ 复制
        Parameters
        ----------
        src  : 文件路径
        dest : 目标路径
    """
    try:
        os.rename(src, dest)
    except Exception as e:
        logging.error('rename file fail\r\n %s' % e)
    else:
        logging.info('rename file success\r\n')


def remove(src):
    """ 删除
        Parameters
        ----------
        src  : 文件路径
    """
    if not os.path.isfile(src):
        logging.error("%s not exist!" % (src))
    else:
        os.remove(src)
        logging.debug("remove %s" % src)


def uncompress(src, dest):
    """ 解压缩
        Parameters
        ----------
        src  : 文件路径
        dest : 目标路径
    """
    if not os.path.isfile(src):
        logging.error("%s not exist!" % (src))
    else:
        unc = zipfile.ZipFile(src)
        unc.extractall(path=dest)
        unc.close()


def compress(src, dest, suffix='zip'):
    """ 压缩
        Parameters
        ----------
        src    : 文件路径
        dest   : 目标路径
        suffix : 压缩格式
    """
    compress = ['.zip', '.rar']
    src = os.path.abspath(src)
    suffix = '.' + suffix.lstrip('.')
    if os.path.isdir(src):
        if (os.path.splitext(dest)[1] not in compress):
            dirname = os.path.split(src)[1]
            dest = os.path.join(dest, (dirname + suffix))
        newZip = zipfile.ZipFile(dest, 'a')
        for dirpath, dirnames, filenames in os.walk(src):
            for dirname in dirnames:
                dp = filepath = os.path.join(dirpath, dirname)
                newZip.write(dp, dp[len(src):])
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                newZip.write(filepath, filepath[len(src):])
    elif os.path.isfile(src):
        if (os.path.splitext(dest)[1] not in compress):
            filename = os.path.splitext(src)
            filename = os.path.split(filename[0])[1]
            dest = os.path.join(dest, (filename + suffix))
        newZip = zipfile.ZipFile(dest, 'a')
        newZip.write(src, src[len(os.path.split(src)[0]):])
    else:
        logging.info("%s is not supported" % src)
    newZip.close()
    logging.info('compress is successed -> %s' % dest)


def get_type_name(filename):
    """
    获取文件路径中的文件名称后缀
    Parameters
    ----------
    filename 文件路径或文件名称

    Returns 如  .png,.txt
    -------

    """
    return os.path.splitext(filename)[1]
