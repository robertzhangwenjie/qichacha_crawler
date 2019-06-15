#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/15 9:02
# @Author   :   robert
# @FileName :   requests_executor.py
# @Software :   PyCharm
import bs4
import requests
from Tools.demo.ss1 import center
from bs4 import BeautifulSoup
import lxml


def get_info_by_request(company_name,cookies):
    '''
    根据公司名称，发起请求获得公司的基本信息
    :param company_name:
    :return:
    '''
    base_url = 'https://www.qichacha.com/search?key='
    url = base_url + company_name

    headers = {
        'Cookie': cookies,
        'Connection': 'keep-alive',
        'Host' : 'www.qichacha.com',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }
    res = requests.get(url,headers=headers)
    bs = BeautifulSoup(res.text, "lxml")
    try:
        company_name_str = bs.find(id='search-result').find('tr')
        # company_name_bs = bs.find(id='search-result').select('#search-result > tr:nth-of-type(1) > td:nth-of-type(3)')
        company_name_bs = company_name_str.find_all('td')[2]
    except Exception as err:
        print(f'获取企业信息失败:{company_name}')
        company_name_bs = ''
    return company_name_bs

if __name__ == '__main__':
    pass




