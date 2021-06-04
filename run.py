#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/15 18:34
# @Author   :   robert
# @FileName :   run.py
# @Software :   PyCharm

'''
爬虫引擎有两个
1.ScrapyerWithRequests
    需要传入cookies
    --推荐使用
    注意点: 要先手动登录，然后获取cookies
'''
import settings

if __name__ == '__main__':
    from src.cralwer import ScrapyerWithRequests

    zg = "%7B%22sid%22%3A%201622765356388%2C%22updated%22%3A%201622766052136%2C%22info%22%3A%201622736675366%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%22a0837e69976465d89af6b5c91388153a%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D"
    cookies = f'QCCSESSID=aoklpnctdmlgbhhbhbq2lnikv6; UM_distinctid=179d2a4a2081a-0140bf75aa57b7-f7f1939-144000-179d2a4a20964f; zg_did=%7B%22did%22%3A%20%22179d2a4a21e166-07cd8ce91cc8cc-f7f1939-144000-179d2a4a21f79c%22%7D; _uab_collina=162273667575028205137258; acw_tc=7d5e319c16227653565704033e68794ce7a5c462ca8490c95e703ada66; CNZZDATA1254842228=671786925-1622735547-%7C1622762548; acw_sc__v2=60b96f357d5f05690776c085abb0a97a74b3ba73; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f="{zg}"'
    runner = ScrapyerWithRequests(cookies=cookies, search_url=settings.SEARCH_URL)
    runner.run()
