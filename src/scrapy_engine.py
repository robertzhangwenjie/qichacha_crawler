#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/15 17:56
# @Author   :   robert
# @FileName :   scrapy_engine.py
# @Software :   PyCharm
from src.company_source_info import CompanyBasicInfo
from src.company_info import get_company_infos
from src.selenium_executor import ScraperWithSelenium
from src.company_excel import CompanyExcel
from src.requests_executor import get_info_by_request


class Scrapyer(object):
    '''
    scrapy engine
    '''

    def __init__(self,get_info_func,cookies=None):
        '''

        :param get_info_func:不同引擎用来获取公司基本信息的函数
        :param cookies: 对于需要cookes的传递cookies
        '''

        # 用来解析html或者element.Tag获取公司信息
        self.get_info_by_html = get_company_infos
        self.cookies = cookies
        # 初始化信息提取函数
        self.get_info_func = get_info_func

    def _get_company_info(self):
        '''
        获取需要抓取的公司的基本信息
        :return:公司信息的一个字典
        '''
        print('获取爬取对象的基本信息')
        company_info_dict = {}
        # 创建一个公司信息对象
        company = CompanyBasicInfo()
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
            _company_info = get_info_func(company_name, self.cookies)

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



class ScrapyerWithRequests(Scrapyer):

    def __init__(self,cookies):
        '''

        :param cookies: 需要传递登录后的cookies
        '''
        self.get_info_func = get_info_by_request
        super(ScrapyerWithRequests, self).__init__(self.get_info_func)
        self.cookies = cookies




class ScrapyerWithSelenium(Scrapyer):

    def __init__(self,base_url='https://www.qichacha.com'):
        self.scrapy = ScraperWithSelenium(base_url)
        self.get_info_func = self.scrapy._get_company_info
        super(ScrapyerWithSelenium, self).__init__(self.get_info_func)
        # 自动登录
        self.scrapy.login()
        # 手动登录
        # login_flag = input('正在手动登录，请输入y或Y进行登录确认:')
        # if login_flag not in ('y','Y'):
        #     raise ValueError('登录失败')





if __name__ == '__main__':
    base_url = 'https://www.qichacha.com'
    cookies = 'acw_tc=7909f42815593172890043685e75a14e702b0dfcfec1e138924a4a756b; zg_did=%7B%22did%22%3A%20%2216b105fe733ab-0b47b45a8b01c8-3b604b0a-144000-16b105fe7344f9%22%7D; UM_distinctid=16b105fe75c25d-0ae12f98b15654-3b604b0a-144000-16b105fe75d93d; _uab_collina=155934785002814269355557; QCCSESSID=e1b226u9k9ep47jfps6i7vvb74; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1560263957,1560264137,1560560102,1560560219; acw_sc__v3=5d04bcda00cf6beca6cd9fd6642b76f954b5ed5a; acw_sc__v2=5d04bcdad4ce8f63da86d64e92374fb70e58a956; CNZZDATA1254842228=72162867-1559343956-%7C1560591556; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560591891; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560591581997%2C%22updated%22%3A%201560591899520%2C%22info%22%3A%201560263956853%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d07d0dce843c5c059aeee45c5acd4e27%22%7D'
    runner = ScrapyerWithRequests(cookies)
    runner.run()