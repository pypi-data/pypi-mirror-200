"""
@File       :   setup.py
@Author     :   cqs
@Time       :   2021-10-9 17:22
@Version    :   1.0
@Contact    :   cqs363@163.com
@Detect       :   None
"""

from setuptools import setup, find_packages  # 这个包没有可以pip一下

setup(
    name="xsCorePy",  # 这个是pip项目发布的名称
    version="1.0.5",  # 版本号，pip默认安装最新版
    keywords=("utils", "xsCorePy"),
    description="模块描述",
    long_description="1.添加日期工具类 2.添加json工具类",
    license="MIT Licence",

    url="https://github.com/yibo7/xsCorePy",  # 项目相关文件地址，一般是github，有没有都行吧
    author="cqs263",
    author_email="cqs363@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["configparser","requests","pycryptodome","apscheduler","sqlalchemy","chardet","dataclasses-json"]  # 该模块需要的第三方库
)
