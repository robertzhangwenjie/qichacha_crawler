#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/2 11:24
# @Author   :   robert
# @FileName :   run.py
# @Software :   PyCharm
import settings
from src.company_info import CompanyInfo
from src.crawler import Crawler
import os

if __name__ == '__main__':
    from src.excel_company import ExcelCompany

    base_url = 'https://www.qichacha.com'
    scrapy = Crawler(base_url)
    # 自动登录
    scrapy.login()
    # 手动登录
    # login_flag = input('正在手动登录，请输入y或Y进行登录确认:')
    # if login_flag not in ('y','Y'):
    #     raise ValueError('登录失败')

    company = CompanyInfo()
    # 获取需要爬取的公司列表
    company_list = company.get_company_names()
    # 获取公司信息表的名称
    excel_name = company.get_excel_name().split('.')[0]
    company_info_list = []
    # 初始化一个data表用来保存数据，名称与source表的名称一致
    company_excel = ExcelCompany(excel_name)
    excel_path = company_excel.generate_excel()

    for num,company_name in enumerate(company_list):
        _company_info = scrapy._get_company_info(company_name)
        # 如果搜索不到该公司则跳到下一家
        if not _company_info:
            continue
        company_info = scrapy.get_company_info(_company_info)
        company_info_list.append(company_info)
        if len(company_info_list) >= 10:
            company_excel.save_data(excel_path,company_info_list)
            company_info_list = []
        # 如果结束时，company_info_list的数量小于10，则把剩下的添加进去
        if num+1 == len(company_list):
            company_excel.save_data(excel_path,company_info_list)



