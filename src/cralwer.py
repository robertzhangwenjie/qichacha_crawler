#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/15 17:56
# @Author   :   robert
# @FileName :   cralwer.py
# @Software :   PyCharm
import requests
from bs4 import BeautifulSoup

import settings
from src.company_source import ExcelCompanySource
from src.company import Company
from src.company_excel import CompanyExcel


class Cralwer(object):
    '''
    scrapy engine base class
    '''

    def __init__(self,get_info_func,cookies=None):
        '''

        :param get_info_func:不同引擎用来获取公司基本信息的函数
        :param cookies: 对于需要cookes的传递cookies
        '''

        # 用来解析html或者element.Tag获取公司信息
        self.get_info_by_html = Company.get_info_list
        self.cookies = cookies
        # 初始化信息提取函数
        self.get_info_func = get_info_func

    def _get_company_info(self):
        '''
        获取需要抓取的公司的基本信息
        :return:公司信息的一个字典
        '''
        company_info_dict = {}
        # 创建一个公司信息对象
        company = ExcelCompanySource()
        # 获取需要爬取的公司列表
        company_list = company.get_company_names()
        # 获取公司信息表的名称
        excel_name = company.get_excel_name().split('.')[0]
        # 初始化一个data表用来保存数据，名称与source表的名称一致
        company_excel = CompanyExcel(excel_name)
        excel_path = company_excel.generate_excel()

        company_info_dict['company_list'] = company_list
        company_info_dict['excel_path'] = excel_path
        company_info_dict['company_excel'] = company_excel

        return company_info_dict

    def _save_company_info(self,company_info_dict,get_info_func):
        '''

        :param company_info_dict: 公司的基本信息字典
        :param get_info_func: 用来解析公司html或者element.Tag的函数
        :return:
        '''
        company_info_list = []
        company_list = company_info_dict['company_list']
        excel_path = company_info_dict['excel_path']
        company_excel = company_info_dict['company_excel']

        for num, company_name in enumerate(company_list):
            # 获取公司信息的bs4.element.Tag对象
            _company_info = get_info_func(company_name)

            if not _company_info:
                continue

            # 获取公司的信息
            company_info = self.get_info_by_html(_company_info)

            company_info_list.append(company_info)
            if len(company_info_list) >= 10:
                company_excel.save_data(excel_path, company_info_list)
                company_info_list = []
            # 如果结束时，company_info_list的数量小于10，则把剩下的添加进去
            if num + 1 == len(company_list):
                company_excel.save_data(excel_path, company_info_list)

    def run(self):
        '''
        启动爬虫
        :return:
        '''
        __company_info__dict = self._get_company_info()
        self._save_company_info(__company_info__dict, self.get_info_func)

class ScrapyerWithRequests(Cralwer):
    '''
    使用requests库进行爬取
    '''

    def __init__(self,cookies,search_url):
        '''
        :param cookies: 需要传递登录后的cookies
        '''
        self.cookies = cookies
        self.search_url = search_url
        super().__init__(self._get_info,self.cookies)

    def _get_info(self,company_name):
        '''
        根据公司名称，发起请求获得公司的基本信息
        :param company_name:
        :return:
        '''
        print(f"开始爬取{company_name}")
        url = self.search_url + company_name

        headers = {
            'Cookie': self.cookies,
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        bs = BeautifulSoup(res.text, "lxml")
        try:
            company_bs = bs.find("table", class_="ntable ntable-list").find('tr')
            # company_name_bs = bs.find(id='search-result').select('#search-result > tr:nth-of-type(1) > td:nth-of-type(3)')
            # company_name_bs = company_name_str.find_all('td')[2]
        except Exception as err:
            print(f'获取 {company_name} 信息失败，url："{url}"')
            company_bs = ''
        return company_bs






if __name__ == '__main__':
    pass