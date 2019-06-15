#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/2 11:24
# @Author   :   robert
# @FileName :   runner_old.py
# @Software :   PyCharm
import settings
from src.company_basic_info import CompanyBasicInfo
from src.selenium_executor import ScraperWithSelenium
import os

from src.company_excel import CompanyExcel
from src.requests_executor import get_info_by_request

class RunnerWithRequests(object):

    def __init__(self):
        self.get_company_info = ScraperWithSelenium.get_company_info

    def run(self,cookies):
        # 创建一个公司信息对象
        company = CompanyBasicInfo()
        # 获取需要爬取的公司列表
        company_list = company.get_company_names()
        # 获取公司信息表的名称
        excel_name = company.get_excel_name().split('.')[0]
        # 初始化一个data表用来保存数据，名称与source表的名称一致
        company_excel = CompanyExcel(excel_name)
        excel_path = company_excel.generate_excel()


        company_info_list = []

        for num,company_name in enumerate(company_list):
            _company_info = get_info_by_request(company_name,cookies)
            company_info = self.get_company_info(_company_info)

            if not company_info:
                continue
            company_info_list.append(company_info)
            if len(company_info_list) >= 10:
                company_excel.save_data(excel_path,company_info_list)
                company_info_list = []
            # 如果结束时，company_info_list的数量小于10，则把剩下的添加进去
            if num+1 == len(company_list):
                company_excel.save_data(excel_path,company_info_list)


class RunnerWithSelenium(object):

    def __init__(self,base_url):
        self.scrapy = ScraperWithSelenium(base_url)
        # 自动登录
        self.scrapy.login()
        # 手动登录
        # login_flag = input('正在手动登录，请输入y或Y进行登录确认:')
        # if login_flag not in ('y','Y'):
        #     raise ValueError('登录失败')


    def run(self):
        # 创建一个公司信息对象
        company = CompanyBasicInfo()
        # 获取需要爬取的公司列表
        company_list = company.get_company_names()
        # 获取公司信息表的名称
        excel_name = company.get_excel_name().split('.')[0]
        # 初始化一个data表用来保存数据，名称与source表的名称一致
        company_excel = CompanyExcel(excel_name)
        excel_path = company_excel.generate_excel()


        company_info_list = []

        for num,company_name in enumerate(company_list):
            _company_info = self.scrapy._get_company_info(company_name)
            # 如果搜索不到该公司则跳到下一家
            if not _company_info:
                continue
            company_info = self.scrapy.get_company_info(_company_info)
            company_info_list.append(company_info)
            if len(company_info_list) >= 10:
                company_excel.save_data(excel_path,company_info_list)
                company_info_list = []
            # 如果结束时，company_info_list的数量小于10，则把剩下的添加进去
            if num+1 == len(company_list):
                company_excel.save_data(excel_path,company_info_list)


if __name__ == '__main__':
    base_url = 'https://www.qichacha.com'
    runner = RunnerWithRequests()
    cookies = 'acw_tc=7909f42815593172890043685e75a14e702b0dfcfec1e138924a4a756b; zg_did=%7B%22did%22%3A%20%2216b105fe733ab-0b47b45a8b01c8-3b604b0a-144000-16b105fe7344f9%22%7D; UM_distinctid=16b105fe75c25d-0ae12f98b15654-3b604b0a-144000-16b105fe75d93d; _uab_collina=155934785002814269355557; QCCSESSID=e1b226u9k9ep47jfps6i7vvb74; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1560263957,1560264137,1560560102,1560560219; acw_sc__v3=5d04bcda00cf6beca6cd9fd6642b76f954b5ed5a; acw_sc__v2=5d04bcdad4ce8f63da86d64e92374fb70e58a956; CNZZDATA1254842228=72162867-1559343956-%7C1560591556; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560591891; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560591581997%2C%22updated%22%3A%201560591899520%2C%22info%22%3A%201560263956853%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d07d0dce843c5c059aeee45c5acd4e27%22%7D'
    runner.run(cookies)




