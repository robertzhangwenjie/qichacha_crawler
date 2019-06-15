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
2.ScrapyerWithSelenium
    使用selenium时，企查查如果判断是自动化工具会导致拖动条验证时无限失败
'''



if __name__ == '__main__':
    from src.scrapy_engine import ScrapyerWithRequests, ScrapyerWithSelenium
    cookies = 'acw_tc=7909f42815593172890043685e75a14e702b0dfcfec1e138924a4a756b; zg_did=%7B%22did%22%3A%20%2216b105fe733ab-0b47b45a8b01c8-3b604b0a-144000-16b105fe7344f9%22%7D; UM_distinctid=16b105fe75c25d-0ae12f98b15654-3b604b0a-144000-16b105fe75d93d; _uab_collina=155934785002814269355557; QCCSESSID=e1b226u9k9ep47jfps6i7vvb74; CNZZDATA1254842228=72162867-1559343956-%7C1560603994; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1560264137,1560560102,1560560219,1560604285; acw_sc__v3=5d04fb4b4a60e54126256f9780fe644eb506b683; acw_sc__v2=5d04fb486ee8d43e7448f17538d4592e476166e9; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560608844; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560604284614%2C%22updated%22%3A%201560608848328%2C%22info%22%3A%201560263956853%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d07d0dce843c5c059aeee45c5acd4e27%22%7D'
    runner = ScrapyerWithRequests(cookies)
    runner.run()