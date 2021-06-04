#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/5/31 23:51
# @Author   :   robert
# @FileName :   settings.py
# @Software :   PyCharm

import os

# 项目根目录
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# 公司信息的excel路径
COMPANY_INFO_PATH_DIR= os.path.join(PROJECT_DIR,'source')

# data路径
COMPANY_DATA_DIR = os.path.join(PROJECT_DIR, 'data')

# drivers路径
WEBDRIVER_PATH = os.path.join(PROJECT_DIR,'webdrivers')

# Webdriver驱动
FireFoxWebdriver = os.path.join(WEBDRIVER_PATH, 'geckodriver.exe')
# Chromedriver驱动
ChromeWebdriver = os.path.join(WEBDRIVER_PATH, 'chromedriver-75.exe')


# 验证码错误最大次数
CODE_INPUT_ERROR_TIMES = 5

# 企查查查询url
SEARCH_URL= 'https://www.qcc.com/web/search?key='

# 登录账号
USERNAME = '***'
PASSWORD = '****'
