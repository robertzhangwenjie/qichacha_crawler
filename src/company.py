#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 15:30
# @Author   :   robert
# @FileName :   company.py
# @Software :   PyCharm
import json
import re

import bs4
from bs4 import BeautifulSoup


class Company(object):
    '''
        企业信息解析对象，对传入的html或者element.Tag对象进行解析
    '''

    def __init__(self, company_html):
        '''
        :param company_html: 传入公司的html对象或者bs4.element.Tag对象
        '''
        self.bs = BeautifulSoup(company_html, 'html.parser') if not isinstance(company_html,
                                                                               bs4.element.Tag) else company_html
        self.company_info = self.bs.find("div", class_="maininfo")
        self.relate_info = self.company_info.find_all("span", class_="val")

    @property
    def name(self):
        '''
        企业名称
        :return:
        '''
        try:
            company_name = self.company_info.find("a", class_="title").text
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
            company_leader = self.relate_info[0].text
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
            company_registry_capital = self.relate_info[1].text
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
            company_registry_date = self.relate_info[2].text
        except Exception as err:
            print(f'找不到注册日期:{err}')
            company_registry_date = '-'
        return company_registry_date

    @property
    def phone(self):
        try:
            company_phone_num = self.relate_info[3].text
        except Exception as err:
            print(f'找不到企业电话:{err}')
            company_phone_num = '-'
        return company_phone_num

    @property
    def email(self):
        try:
            company_email = self.company_info.find("a", class_="val").text
        except Exception as err:
            print(f'找不到企业邮箱:{err}')
            company_email = '-'
        return company_email

    @property
    def more_phone(self):
        try:
            company_more_phone_attr = self.company_info[1].find('a')['onclick']
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
            print('更多电话获取失败')
            company_more_phone = []
        return company_more_phone

    @property
    def addr(self):
        try:
            company_addr = self.relate_info[-1].text
        except Exception as err:
            print(f'公司地址获取失败:{err}')
            company_addr = '-'
        return company_addr

    @property
    def scope(self):
        '''
        企业经营范围
        :return:
        '''
        try:
            _company_scope = self.company_info.find_all("span", class_="sf")[1].text
            company_scope = re.search("一般经营项目是:(.*)", _company_scope).group(1)
            print(company_scope)
        except Exception as err:
            print(f'公司经营范围获取失败:{err}')
            company_scope = '-'
        return company_scope

    @staticmethod
    def get_info_list(company_info_html):
        '''
        根据传入的对象，获取企业的相关信息
        :param company_info_html: 公司信息的html_str或者是bs.element.Tag对象
        :return: 公司信息的list
        '''
        # 初始化公司信息
        company_info_list = []
        company_info = Company(company_info_html)

        # 公司名称
        company_name = company_info.name
        company_info_list.append(company_name)

        # 法人代表
        company_legal_person = company_info.leader
        company_info_list.append(company_legal_person)

        # 注册资金
        company_registered_capital = company_info.registry_capital
        company_info_list.append(company_registered_capital)

        # 成立日期
        company_registered_date = company_info.registry_date
        company_info_list.append(company_registered_date)

        # 邮箱
        company_email = company_info.email
        company_info_list.append(company_email)

        # 电话
        company_phone = company_info.phone
        company_info_list.append(company_phone)

        # 更多电话
        company_more_phone = company_info.more_phone
        company_info_list.append(company_more_phone)

        # 地址
        company_addr = company_info.addr
        company_info_list.append(company_addr)

        # 经营范围
        company_scope = company_info.scope
        company_info_list.append(company_scope)

        print(company_info_list)
        return company_info_list


if __name__ == '__main__':
    pass
