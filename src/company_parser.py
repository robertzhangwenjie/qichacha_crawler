#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 15:30
# @Author   :   robert
# @FileName :   company.py
# @Software :   PyCharm
import json
import re
import pickle

import bs4
from bs4 import BeautifulSoup

class CompanyInfoParser(object):
    '''
        企业信息解析对象，对传入的html或者element.Tag对象进行解析
    '''

    def __init__(self,company_html):
        '''
        :param company_html: 传入公司的html对象或者bs4.element.Tag对象
        '''
        self.bs = BeautifulSoup(company_html,'html.parser') if not isinstance(company_html, bs4.element.Tag) else company_html
        self.company_infos = self.bs.find_all('p')

    @property
    def name(self):
        '''
        企业名称
        :return:
        '''
        try:
            company_name = self.bs.find_all('a')[0].text
        except Exception as err:
            print(f'找不到企业名称:{err}')
            company_name = '-'
        return company_name

    @property
    def leader(self):
        '''
        企业负责人或法人
        :return:
        '''
        try:
            company_leader = self.company_infos[0].find('a').text
        except Exception as err:
            print(f'找不到企业负责人或者法人:{err}')
            company_leader = '-'
        return company_leader

    @property
    def registry_capital(self):
        '''
        企业注册资金
        :return:
        '''
        try:
            company_registry_capital = self.company_infos[0].find_all('span')[0].text.split("：")[1]
        except Exception as err:
            print(f'找不到注册资金:{err}')
            company_registry_capital = '-'
        return company_registry_capital

    @property
    def registry_date(self):
        '''
        注册日期
        :return:
        '''
        try:
            company_registry_date = self.company_infos[0].find_all('span')[1].text.split("：")[1]
        except Exception as err:
            print(f'找不到注册日期:{err}')
            company_registry_date = '-'
        return company_registry_date

    @property
    def email(self):

        try:
            company_email = self.company_infos[1].text.strip().split('\n')[0].split("：")[1]
        except Exception as err:
            print(f'找不到企业邮箱:{err}')
            company_email = '-'
        return company_email

    @property
    def phone(self):
        try:
            company_phone_num = self.company_infos[1].find('span').text.split("：")[1]
        except Exception as err:
            print(f'找不到企业电话:{err}')
            company_phone_num = '-'
        return company_phone_num

    @property
    def more_phone(self):
        try:
            company_more_phone_attr =self.company_infos[1].find('a')['onclick']
            # 正则匹配初更多电话的一个json字符串
            _more_phone_list = re.search(r'\[(.*?)\]', company_more_phone_attr).group()
            # 反序列化为python的list
            more_phone_list = json.loads(_more_phone_list)
            # 初始化一个更多电话list
            company_more_phone_list = []
            for phone_dict in more_phone_list:
                # 取出电话号码和对应的日期
                phone_num = phone_dict.get('t', None)
                phone_date = phone_dict.get('s', None)
                # 将电话号码和时间用'-'拼接后放入list
                _more_phone_tuple = phone_num, phone_date
                company_more_phone_list.append('-'.join(_more_phone_tuple))
            company_more_phone = ','.join(company_more_phone_list)
        except Exception as err:
            print(f'更多电话获取失败:{err}')
            company_more_phone = []
        return company_more_phone

    @property
    def addr(self):
        try:
            company_addr = self.company_infos[2].text.strip().split("：")[1]
        except Exception as err:
            print(f'公司地址获取失败:{err}')
            company_addr = '-'
        return company_addr


if __name__ == '__main__':
    pass