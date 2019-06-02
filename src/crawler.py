#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 8:09
# @Author   :   robert
# @FileName :   crawler.py
# @Software :   PyCharm

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from src import common
import settings
from page.qichacha_login_page import QichachaPage
from page.qichacha_home import QichachaHome
from src.company import Company
from src.company_info import CompanyInfo
import settings
class Crawler(object):
    '''爬虫类'''
    def __init__(self,url):
        self.username = settings.USERNAME
        self.password = settings.PASSWORD
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.url = url
        self.qichacha = QichachaPage()
        self.qichacha_home = QichachaHome()

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element(*self.qichacha.login_link).click()
        # 选择密码登录
        self.driver.find_element(*self.qichacha.login_with_password).click()

        # 输入手机号
        self.driver.find_element(*self.qichacha.phone_input).clear()
        self.driver.find_element(*self.qichacha.phone_input).send_keys(settings.USERNAME)

        # 输入密码
        self.driver.find_element(*self.qichacha.password_input).clear()
        self.driver.find_element(*self.qichacha.password_input).send_keys(settings.PASSWORD)

        # 滑动登录
        self.qichacha.scroll_btn_move(self.driver)

        # 输入验证码并登录
        self.qichacha.input_verification_code(self.driver)

        # 登录
        self.driver.find_element(*self.qichacha.login_btn).click()

        # 判断是否有弹框
        bindwx = common.is_element_display(self.driver,self.qichacha_home.bindwx_pop)
        if bindwx:
        # print(bindwx)
        # if bindwx:
        # 关闭弹窗
            self.qichacha_home.close_bindwx(self.driver)

    # 根据公司名称爬取相关信息
    def scrpay_company_info(self,company_name):
        print('开始搜索')
        try:
            self.driver.find_element(*self.qichacha_home.research_input).clear()
            self.driver.find_element(*self.qichacha_home.research_input).send_keys(company_name)
            self.driver.find_element(*self.qichacha_home.research_btn).click()
        except NoSuchElementException as err:
            self.driver.find_element(*self.qichacha_home.search_input).clear()
            self.driver.find_element(*self.qichacha_home.search_input).send_keys(company_name)
            self.driver.find_element(*self.qichacha_home.search_btn).click()


        # 符合条件的第一家公司
        _company_info = self.driver.find_element(*self.qichacha_home.result).get_attribute('innerHTML')

        # 初始化公司信息
        company_info_list = []
        company_info = Company(_company_info)

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

        print(company_info_list)
        return company_info_list

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    from src.excel_company import ExcelCompany
    base_url = 'https://www.qichacha.com'
    scrapy = Crawler(base_url)
    scrapy.login()
    company_list = CompanyInfo(settings.COMPANY_INFO_PATH).get_company_names()
    company_info_list = []
    bulk_size = 0
    company_excel = ExcelCompany('朱蒙')
    excel_path = company_excel.generate_excel()
    for company_name in company_list:
        company_info = scrapy.scrpay_company_info(company_name)
        company_info_list.append(company_info)
        if bulk_size >= 10:
            company_excel.save_data(excel_path,company_info_list)
            company_info_list = []
        bulk_size +=1

