#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 12:21
# @Author   :   robert
# @FileName :   qichacha_home.py
# @Software :   PyCharm
from selenium.webdriver.common.by import By

from src import common
class QichachaHome(object):

    # 微信绑定弹出框
    bindwx_pop = By.CLASS_NAME,'bindwx'
    # 弹出框关闭按钮
    bindwx_close_btn = By.CSS_SELECTOR,'#bindwxModal > div > div > div > button'

    # 第一次搜索框
    search_input = By.ID,'searchkey'
    #第二次搜索框
    research_input = By.ID,'headerKey'

    # 搜索结果的第一个的第三个td
    result = By.CSS_SELECTOR,'#search-result > tr:nth-child(1) > td:nth-child(3)'
    #第一次搜索按钮
    search_btn = By.ID,'V3_Search_bt'
    #第二次搜索按钮
    research_btn = By.CSS_SELECTOR,'body > header > div > form > div > div > span > button'

    def close_bindwx(self,driver):
        js = "document.getElementsByClassName('close')[0].click()"
        driver.execute_script(js)
        if common.is_element_exist(driver,self.bindwx_pop):
            flag = input('请删除完成后输入y|Y')


