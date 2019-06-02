#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 15:30
# @Author   :   robert
# @FileName :   company.py
# @Software :   PyCharm
import json
import re
import pickle
from bs4 import BeautifulSoup

class Company(object):
    '''
        提取公司的部分信息
    '''


    def __init__(self,company_html):
        '''
        :param company_html: 传入公司的html对象
        '''
        self.bs = BeautifulSoup(company_html,'html.parser')
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
    s = '''<td> <a onclick="zhugeTrack('查企业-搜索列表页-查看企业',{'企业名称':'深圳市<em>法本</em><em>信息</em>技术股份有限公司上海分公司'});addSearchIndex('法本信息',2,'%E6%B7%B1%E5%9C%B3%E5%B8%82%3Cem%3E%E6%B3%95%E6%9C%AC%3C%2Fem%3E%3Cem%3E%E4%BF%A1%E6%81%AF%3C%2Fem%3E%E6%8A%80%E6%9C%AF%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E4%B8%8A%E6%B5%B7%E5%88%86%E5%85%AC%E5%8F%B8');" href="/firm_352843856d4a5636ae69515182d17c7c.html" target="_blank" class="ma_h1">深圳市<em>法本</em><em>信息</em>技术股份有限公司上海分公司</a> <div class="search-tags"> </div> <p class="m-t-xs">
                                                                                                                                                                负责人：
                                                                                                                                                                                                                <a onclick="zhugeTrack('查企业-搜索列表页-查看法定代表人',{'人物名称':'严华'});" class="text-primary" href="/pl_p2f8a26e4ff50502f4cb5a1c6abdd11f.html">严华</a> <span class="m-l">注册资本：-</span> <span class="m-l">成立日期：2008-02-26</span> </p> <p class="m-t-xs">
                                        邮箱：sh.hr@farben.com.cn
                                        <span class="m-l">电话：021-32516951</span> <a class="text-primary" onclick="showHisTel([{&quot;t&quot;:&quot;021-32516951&quot;,&quot;s&quot;:&quot;2018&quot;},{&quot;t&quot;:&quot;021-32516956&quot;,&quot;s&quot;:&quot;2017&quot;}],&quot;021-32516951&quot;);">更多号码</a> </p> <p class="m-t-xs">
                                        地址：上海市长宁区金钟路968号3号楼1002室
                                    </p> <p></p> </td>'''

    bs = BeautifulSoup(s,'html.parser')

    # 企业负责人
    print(bs.find_all('p')[0].find_all('a')[0].text)
    # 企业注册资本
    print(bs.find_all('p')[0].find_all('span')[0].text.split("：")[1])
    # 企业成立日期
    print(bs.find_all('p')[0].find_all('span')[1].text.split("：")[1])
    # 企业邮箱
    print(bs.find_all('p')[1].text.strip().split('\n')[0].split("：")[1])
    # 企业电话
    print(bs.find_all('p')[1].find('span').text.split("：")[1])
    # 更多电话--通过获取属性值在进行解析
    _more_phone = bs.find_all('p')[1].find('a')['onclick']
    _more_phone_list = re.search(r'\[(.*?)\]',_more_phone).group()
    more_phone_list = json.loads(_more_phone_list)
    more_phone_list_ok = []
    for phone_dict in more_phone_list:
            phone_num = phone_dict.get('t',None)
            phone_date = phone_dict.get('s',None)
            _more_phone_tuple = phone_num,phone_date
            more_phone_list_ok.append(_more_phone_tuple)
    print(more_phone_list_ok)
    # 企业地址
    company_addr = bs.find_all('p')[2].text.strip().split("：")[1]
    print(company_addr)