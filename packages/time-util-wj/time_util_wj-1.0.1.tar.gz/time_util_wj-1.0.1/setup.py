# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/3/30 16:26
# @Author : wangjie
# @File : setup.py
# @project : Automation

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="time_util_wj",  # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="1.0.1",  # 程序版本
    author="WangJie",  # 项目作者
    author_email="1641540482@qq.com",  # 作者邮件
    description="提供了各种时间转换的方法",  # 项目的一句话描述
    long_description=long_description,  # 加长版描述
    long_description_content_type="text/markdown",  # 描述使用Markdown
    url="https://github.com/wangjie-jason",  # 项目地址
    packages=setuptools.find_packages(),  # 无需修改
    classifiers=[
        "Programming Language :: Python :: 3",  # 使用Python3
        "License :: OSI Approved :: Apache Software License",  # 开源协议
        "Operating System :: OS Independent",
    ],
)